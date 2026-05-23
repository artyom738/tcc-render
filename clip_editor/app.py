from flask import Flask, render_template, request, jsonify, send_from_directory
import sys
import os

# Добавляем родительскую директорию в путь для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.repository.song_repository import song_repository
from model.repository.chart_repository import chart_repository
from model.repository.position_repository import position_repository
from model.repository.chart_rubrics_repository import chart_rubric_repository
from model.entity.chart import Chart
from model.entity.position import Position
from model.entity.rubric import Rubric
from model.entity.song import Song
from db import database

app = Flask(__name__)

# Путь к папке с клипами
CLIPS_FOLDER = r'D:\Artyom\Проекты\Top Club Chart\клипы чарта\regulars'

# Конфигурация типов чартов для веб-редактора
CHART_TYPE_CONFIG = {
	'tcc': {
		'positions_count': 26,
		'rubric_slots': [
			{'code': chart_rubric_repository.RUBRIC_RESIDANCE, 'label': 'Residance'},
			{'code': chart_rubric_repository.RUBRIC_PERSPECTIVE, 'label': 'Perspective'},
			{'code': chart_rubric_repository.RUBRIC_ALL_TIME, 'label': 'All-time'},
		],
	},
	'eht': {
		'positions_count': 40,
		'rubric_slots': [
			{'code': chart_rubric_repository.RUBRIC_EHT_PERSPECTIVE, 'label': 'Новое'},
			{'code': chart_rubric_repository.RUBRIC_EHT_OLD, 'label': 'Прошлое'},
		],
	},
}


def _chart_date_to_str(value):
	if value is None:
		return ''
	if hasattr(value, 'isoformat'):
		return value.isoformat()
	return str(value)


def _serialize_positions(rows):
	return [{
		'position': row['POSITION'],
		'song_id': row['SONG_ID'],
		'name': row.get('NAME') or '',
		'authors': row.get('AUTHORS') or '',
	} for row in rows]


def _serialize_rubrics(rows):
	return [{
		'rubric_type': row['RUBRIC_TYPE'],
		'song_id': row['SONG_ID'],
		'name': row.get('NAME') or '',
		'authors': row.get('AUTHORS') or '',
	} for row in rows]


@app.route('/')
def index():
	"""Главная страница со списком песен"""
	query = 'SELECT ID, AUTHORS, NAME, CLIP_PATH, EP_ID FROM songs WHERE CLIP_PATH IS NOT NULL AND CLIP_PATH != "" ORDER BY ID DESC LIMIT 100'
	songs = database.get_list(query)
	return render_template('clip_editor_index.html', songs=songs, active_page='editor')


@app.route('/api/search')
def search_songs():
	"""API для поиска песен"""
	search_term = request.args.get('q', '').strip()

	if not search_term:
		query = 'SELECT ID, AUTHORS, NAME, CLIP_PATH, EP_ID FROM songs WHERE CLIP_PATH IS NOT NULL AND CLIP_PATH != "" ORDER BY ID DESC LIMIT 100'
		songs = database.get_list(query)
	else:
		# Поиск по ID, имени исполнителя или названию песни
		query = '''
			SELECT ID, AUTHORS, NAME, CLIP_PATH, EP_ID
			FROM songs 
			WHERE CLIP_PATH IS NOT NULL AND CLIP_PATH != ""
			AND (
				CAST(ID AS CHAR) LIKE %s
				OR LOWER(AUTHORS) LIKE %s
				OR LOWER(NAME) LIKE %s
			)
			ORDER BY ID DESC
			LIMIT 100
		'''
		search_pattern = f'%{search_term}%'
		songs = database.get_list(query, (search_pattern, search_pattern, search_pattern))

	return jsonify({'songs': songs})


@app.route('/editor/<int:song_id>')
def editor(song_id):
	"""Страница редактора для конкретной песни"""
	song = song_repository.get_song_by_id(song_id)
	if not song:
		return "Песня не найдена", 404

	return render_template('clip_editor.html', song=song, active_page='editor')


@app.route('/api/song/<int:song_id>')
def get_song(song_id):
	"""API для получения данных песни"""
	song = song_repository.get_song_by_id(song_id)
	if not song:
		return jsonify({'error': 'Song not found'}), 404

	return jsonify({
		'id': song.id,
		'name': song.name,
		'authors': song.authors,
		'clip_path': song.clip_path,
		'clip_name': song.clip_name,
		'start_times': song.clip_start_sec,
		'end_times': song.clip_end_sec
	})


@app.route('/api/song/<int:song_id>/save', methods=['POST'])
def save_song_times(song_id):
	"""API для сохранения таймингов песни"""
	data = request.json
	start_times = data.get('start_times', [])
	end_times = data.get('end_times', [])

	# Валидация данных
	if len(start_times) != len(end_times):
		return jsonify({'error': 'Start and end times count mismatch'}), 400

	for i in range(len(start_times)):
		if start_times[i] >= end_times[i]:
			return jsonify({'error': f'Start time must be less than end time for segment {i+1}'}), 400

	# Формирование строк для БД
	start_times_str = ','.join([str(t) for t in start_times]) if start_times else None
	end_times_str = ','.join([str(t) for t in end_times]) if end_times else None

	# Обновление в БД
	query = 'UPDATE songs SET CLIP_START_SEC = %s, CLIP_END_SEC = %s WHERE ID = %s'
	database.execute_query(query, (start_times_str, end_times_str, song_id))

	return jsonify({'success': True, 'message': 'Times saved successfully'})


@app.route('/clips/<path:filename>')
def serve_clip(filename):
	"""Обслуживание видеофайлов из локальной папки"""
	return send_from_directory(CLIPS_FOLDER, filename)


# region Chart Builder

@app.route('/chart_builder')
def chart_builder():
	"""Страница ручного составления чарта"""
	return render_template('chart_builder.html', chart_type_config=CHART_TYPE_CONFIG, active_page='chart_builder')


@app.route('/api/chart_builder/search')
def chart_builder_search():
	"""Поиск песен для перетаскивания в чарт (по NAME и AUTHORS, без фильтра по клипам)"""
	query = request.args.get('q', '').strip()
	songs = song_repository.search(query, limit=50)

	return jsonify({'songs': [{
		'id': song.id,
		'name': song.name,
		'authors': song.authors,
		'ep_id': song.ep_id,
		'has_clip': bool(song.clip_name),
	} for song in songs]})


@app.route('/api/chart_builder/song', methods=['POST'])
def chart_builder_create_song():
	"""Создание новой песни вручную (только название + автор, EP_ID = NULL)"""
	data = request.json or {}
	name = (data.get('name') or '').strip()
	authors = (data.get('authors') or '').strip()

	if not name or not authors:
		return jsonify({'error': 'Поля name и authors обязательны'}), 400

	song = Song({
		'name': name,
		'authors': authors,
		'ep_id': None,
	})
	song.save()

	return jsonify({
		'id': song.id,
		'name': song.name,
		'authors': song.authors,
		'ep_id': None,
		'has_clip': False,
	})


@app.route('/api/chart_builder/previous')
def chart_builder_previous():
	"""Возвращает позиции и рубрики последнего чарта данного типа + предлагаемый CHART_NUMBER"""
	chart_type = request.args.get('chart_type', '').strip()
	if chart_type not in CHART_TYPE_CONFIG:
		return jsonify({'error': 'Неизвестный chart_type'}), 400

	next_number = chart_repository.get_next_chart_number(chart_type)
	last_chart = chart_repository.get_last_chart_by_type(chart_type)
	if not last_chart:
		return jsonify({
			'chart_type': chart_type,
			'chart_number': next_number,
			'last_chart': None,
			'positions': [],
			'rubrics': [],
		})

	full = chart_repository.get_full_chart(last_chart.id)

	return jsonify({
		'chart_type': chart_type,
		'chart_number': next_number,
		'last_chart': {
			'id': last_chart.id,
			'chart_number': last_chart.chart_number,
			'chart_date': _chart_date_to_str(last_chart.chart_date),
		},
		'positions': _serialize_positions(full['positions']),
		'rubrics': _serialize_rubrics(full['rubrics']),
	})


@app.route('/api/chart_builder/chart/<int:chart_id>')
def chart_builder_get_chart(chart_id):
	"""Полные данные чарта для режима редактирования"""
	full = chart_repository.get_full_chart(chart_id)
	if not full:
		return jsonify({'error': 'Чарт не найден'}), 404

	chart = full['chart']
	last_chart = chart_repository.get_last_chart_by_type(chart.chart_type)
	last_chart_info = None
	if last_chart:
		last_chart_info = {
			'id': last_chart.id,
			'chart_number': last_chart.chart_number,
			'chart_date': _chart_date_to_str(last_chart.chart_date),
		}
	return jsonify({
		'chart_id': chart.id,
		'chart_type': chart.chart_type,
		'chart_date': _chart_date_to_str(chart.chart_date),
		'chart_number': chart.chart_number,
		'last_chart': last_chart_info,
		'positions': _serialize_positions(full['positions']),
		'rubrics': _serialize_rubrics(full['rubrics']),
	})


@app.route('/api/chart_builder/save', methods=['POST'])
def chart_builder_save():
	"""Сохранение нового чарта или обновление существующего"""
	data = request.json or {}

	chart_type = (data.get('chart_type') or '').strip()
	if chart_type not in CHART_TYPE_CONFIG:
		return jsonify({'error': 'Неизвестный chart_type'}), 400

	chart_date = (data.get('chart_date') or '').strip()
	if not chart_date:
		return jsonify({'error': 'Поле chart_date обязательно'}), 400

	try:
		chart_number = int(data.get('chart_number') or 0)
	except (TypeError, ValueError):
		return jsonify({'error': 'chart_number должен быть числом'}), 400

	positions = data.get('positions') or []
	rubrics = data.get('rubrics') or []

	valid_rubric_codes = {slot['code'] for slot in CHART_TYPE_CONFIG[chart_type]['rubric_slots']}
	positions_count = CHART_TYPE_CONFIG[chart_type]['positions_count']

	# Валидация позиций
	seen_positions = set()
	for item in positions:
		pos = item.get('position')
		song_id = item.get('song_id')
		if not isinstance(pos, int) or pos < 1 or pos > positions_count:
			return jsonify({'error': f'Некорректная позиция: {pos}'}), 400
		if pos in seen_positions:
			return jsonify({'error': f'Позиция {pos} указана дважды'}), 400
		if not isinstance(song_id, int):
			return jsonify({'error': f'Некорректный song_id для позиции {pos}'}), 400
		seen_positions.add(pos)

	# Валидация рубрик: либо song_id, либо name+authors для автосоздания
	seen_rubrics = set()
	for item in rubrics:
		rubric_type = item.get('rubric_type')
		if rubric_type not in valid_rubric_codes:
			return jsonify({'error': f'Некорректный rubric_type: {rubric_type}'}), 400
		if rubric_type in seen_rubrics:
			return jsonify({'error': f'Рубрика {rubric_type} указана дважды'}), 400
		seen_rubrics.add(rubric_type)

		song_id = item.get('song_id')
		if song_id is None:
			name = (item.get('name') or '').strip()
			authors = (item.get('authors') or '').strip()
			if not name or not authors:
				return jsonify({'error': f'Для рубрики {rubric_type} нужно либо song_id, либо name+authors'}), 400
		elif not isinstance(song_id, int):
			return jsonify({'error': f'Некорректный song_id для рубрики {rubric_type}'}), 400

	chart_id = data.get('chart_id')

	# Сохранение / обновление шапки чарта
	chart = Chart({
		'id': chart_id,
		'chart_type': chart_type,
		'chart_number': chart_number,
		'chart_date': chart_date,
	})
	chart.save()

	# Перезапись позиций и рубрик
	if chart_id:
		position_repository.delete_by_chart_id(chart.id)
		chart_rubric_repository.delete_by_chart_id(chart.id)

	for item in positions:
		Position({
			'chart_id': chart.id,
			'song_id': item['song_id'],
			'position': item['position'],
		}).save()

	for item in rubrics:
		song_id = item.get('song_id')
		if song_id is None:
			new_song = Song({
				'name': (item.get('name') or '').strip(),
				'authors': (item.get('authors') or '').strip(),
				'ep_id': None,
			})
			new_song.save()
			song_id = new_song.id
		Rubric({
			'chart_id': chart.id,
			'song_id': song_id,
			'rubric_type': item['rubric_type'],
			'chart_type': chart_type,
		}).save()

	return jsonify({'chart_id': chart.id})

# endregion


if __name__ == '__main__':
	app.run(debug=True, host='127.0.0.1', port=5000)
