# CLAUDE.md

ОТВЕЧАЙ ВСЕГДА НА ТОМ ЯЗЫКЕ, НА КОТОРОМ НАПИСАН ВОПРОС ИЛИ КОММЕНТАРИЙ. НЕ ПЕРЕХОДИ НА АНГЛИЙСКИЙ, ЕСЛИ НЕ ПРОСЯТ.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Pipeline that produces music-chart countdown videos (vertical 1080×1920) for Top Club Chart (`tcc`), Eurohit Top 40 (`eht`), and several seasonal/specialty variants (`dark`, `list`, `eht_ny`, `tcc_ny`). The flow is: pull next chart data from an external source → persist to MySQL → download YouTube clips for any missing songs → render per-position video clips in parallel via MoviePy → concatenate with intro/outro/transitions → write final MP4 to `production/`.

`main.py` is the entry point; switching `chart_type` and toggling `chart_id` between `None` (build a brand-new chart from the connector) and an existing ID (re-render or continue an already-saved chart) is the normal way to drive it.

## Run / test commands

```powershell
# Render a chart — edit chart_type / chart_id / rubrics in main.py first
python main.py

# Tests (uses a separate DB tcc_render_test via TCC_TEST_MODE=1 env var)
python tests\setup_test_db.py setup           # one-time: create test DB
python -m unittest discover tests -v          # run all tests
python -m unittest tests.test_song_repository # run one test module
python tests\check_databases.py               # inspect prod vs. test DB state

# Standalone Flask UI for editing per-song clip start/end timings
python clip_editor\app.py    # then open http://127.0.0.1:5000
```

There is no requirements.txt; key deps include `moviepy`, `librosa`, `numpy`, `pymysql`, `yt-dlp`, `youtubesearchpython`, `flask`, `skimage`. The repo ships its own `ffmpeg.exe` and `yt-dlp.exe` at the project root and uses them directly.

## Database

MySQL/MariaDB at `127.0.0.1` (root, no password — see `db/database.py`). Schema in `db/install.sql`: `charts`, `songs`, `chart_positions`, `chart_rubrics`. Setting `TCC_TEST_MODE=1` swaps every connection to `tcc_render_test` — `db/database.py` is the single switch point, so any module that calls `database.execute_query/get_list/add` is automatically test-mode aware.

## Architecture

Three parallel factory hierarchies, all keyed on the same `chart_type` string (`tcc`, `eht`, `dark`, `list`, `eht_ny`, `tcc_ny`). When adding a new chart type you almost always touch all three:

- **`connectors/`** — `ConnectorFactory` → `BaseConnector` subclasses. Fetch chart data from external sources (Eurohit page, TCC podcast/radio JSON, dark.json, etc.) and persist `Chart` + `chart_positions` + `chart_rubrics` rows. Entry points used by `main.py`: `create_next_chart()`, `save_chart_data()`, `save_rubrics()`.
- **`charts/`** — `ChartFactory` → `BaseChart` subclasses (`TopClubChart`, `Eht40`, `Darknity`, `List`, `EhtNy`, `TccNy`, plus `TccNyPoints` / `EhtNyPoints` / `EhtPretenders` variants). The renderer. `BaseChart.render()` calls `generate_clip()`, which composes: intro → outs → positions → outro, with `tricolor*.mp4` / `round-arrow.mp4` transition overlays from `package/`. Subclasses override hooks like `get_position_text_color`, `need_show_lcs`, `need_show_lw_moving`, `get_additional_stat_info`, `get_intro`, `get_outro_path`.
- **`rubrics/`** — `RubricFinderFactory` for chart-types that auto-pick recurring segments ("New / Past", "Residance / Perspective / All-time"). Currently `tcc` is the only implemented finder; for `eht` the rubrics dict in `main.py` is filled in by hand each week.

### Concurrency in rendering

`BaseChart.get_positions()` uses `concurrent.futures.ProcessPoolExecutor(max_workers=MAX_WORKERS)` (from `config.py`, default 2) to render position clips in parallel; `get_outs()` uses raw `multiprocessing.Process`. Each worker writes one MP4 to `video_parts/{chart_type}/{chart_number}/{position}.mp4`, the parent process re-loads each file, re-normalizes audio to RMS ~0.3 via `librosa`, and concatenates. Bumping `MAX_WORKERS` past available memory will OOM — MoviePy + ffmpeg per worker is heavy.

### Domain model

`model/entity/` (`Chart`, `Position`, `Song`, `Rubric`) + `model/repository/` (singletons like `song_repository`, `chart_repository`). `Chart.fill()` is the canonical way to hydrate a chart after creation/load — it pulls positions and outs from `position_repository`, then runs `fill_max_up_down` (annotates `super-up`/`double-up`/`double-down` movers), `fill_lcs` (Longest Chart Sitter), and `fill_rubrics`. `Song.clip_start_sec` / `clip_end_sec` are stored as comma-separated strings in the DB and parsed into `list[float]` on load — `clip_editor` exists specifically to edit these.

### YouTube clip pipeline

`yt_clip_downloader.fill_songs_with_no_clip()` runs before rendering: for every song lacking a `CLIP_PATH`, it searches YouTube, downloads via `yt-dlp.exe` (cookies in `yt_cookies.txt`), then `chorus_finder/` analyzes audio to auto-detect the chorus start/end and writes those into `CLIP_START_SEC`/`CLIP_END_SEC`. The comment "Download clips - enable VPN first" in `main.py` is real — YouTube blocks the download IP without it.

## Output paths and assets

- Final videos: `production/{chart_type} {YYYY-MM-DD}.mp4`
- Per-position intermediate clips: `video_parts/{chart_type}/{chart_number}/`
- Preview thumbnails for the last "out": `previews/`
- Fonts, intros, outros, overlays, logos: `package/` (gitignored — assets live outside the repo)

## Conventions

- Source files are tab-indented (not spaces) — match existing style when editing.
- Comments, commit messages, and most docstrings are in Russian; keep that style when editing existing files. New top-level docs may be English.
- Repositories are module-level singleton instances (`song_repository = SongRepository()`); import the instance, don't instantiate the class.
- The `chart_type` string is the single source of branching across factories — when introducing a new type, add it to `ConnectorFactory`, `ChartFactory`, and (if it has rubrics) `RubricFinderFactory` in one pass.
