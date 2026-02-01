import os
import shutil

from yt_dlp import YoutubeDL
from yt_dlp.utils import ExtractorError
from youtubesearchpython import VideosSearch

from chorus_finder.finder import ChorusFinder
from terminal_colors import Colors

import chorus_finder
from model.repository.song_repository import song_repository


def find_clip(query, max_results=10):
	try:
		videos_search = VideosSearch(query, limit=max_results)
		results = videos_search.result()
	except Exception as e:
		print(f'{Colors.FAIL}Search error: {e}. Trying with limit=5{Colors.ENDC}')
		try:
			videos_search = VideosSearch(query, limit=5)
			results = videos_search.result()
		except Exception as e2:
			print(f'{Colors.FAIL}Search failed: {e2}{Colors.ENDC}')
			return None

	if not results or 'result' not in results or not results['result']:
		print(f'{Colors.FAIL}No results found for query: {query}{Colors.ENDC}')
		return None

	for song in results['result']:
		# Проверяем наличие необходимых полей
		if not song or 'id' not in song:
			continue
		# Пропускаем канал "Selected" если он есть
		if 'channel' in song and song['channel'] and 'name' in song['channel']:
			if song['channel']['name'] == 'Selected':
				continue
		return song['id']

	# Если все видео отфильтрованы, возвращаем первое
	return results['result'][0]['id'] if results['result'] else None


def download_clip(url: str, min_height=720):
	"""
	Скачивает клип с YouTube, пытаясь получить максимально возможное качество.

	Args:
		url: URL видео на YouTube
		min_height: Минимальная желаемая высота видео (по умолчанию 720)

	Returns:
		dict с путями к скачанному файлу

	Raises:
		ExtractorError: если не удалось скачать видео или качество ниже минимального
	"""
	# Базовые опции без cookies
	base_opts_no_cookies = {
		'keepvideo': False,
		'outtmpl': 'D:/Artyom/Проекты/Top Club Chart/клипы чарта/regulars/%(title)s.%(ext)s',
		'nocheckcertificate': True,
		'http_chunk_size': 10485760,
		'retries': 10,
		'fragment_retries': 10,
		'skip_unavailable_fragments': True,
		'verbose': False,
		'quiet': False,
		'no_warnings': False,
		'merge_output_format': 'mp4',
	}

	# Базовые опции с cookies
	base_opts_with_cookies = {
		**base_opts_no_cookies,
		'cookiefile': 'yt_cookies.txt',
	}

	# Стратегия 1: Android Music клиент - часто работает без токенов для музыкальных видео
	ydl_opts_android_music = {
		**base_opts_no_cookies,
		'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
		'extractor_args': {
			'youtube': {
				'player_client': ['android_music'],
				'player_skip': ['configs', 'webpage'],
			}
		},
	}

	# Стратегия 2: Android SDK-less клиент БЕЗ cookies
	ydl_opts_android_sdkless = {
		**base_opts_no_cookies,
		'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
		'extractor_args': {
			'youtube': {
				'player_client': ['android_sdkless'],
				'player_skip': ['configs'],
			}
		},
	}

	# Стратегия 3: iOS клиент с куками
	ydl_opts_ios_cookies = {
		**base_opts_with_cookies,
		'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
		'extractor_args': {
			'youtube': {
				'player_client': ['ios'],
				'player_skip': ['configs'],
			}
		},
	}

	# Стратегия 4: Web Safari клиент с куками
	ydl_opts_web_safari = {
		**base_opts_with_cookies,
		'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
		'extractor_args': {
			'youtube': {
				'player_client': ['web_safari'],
			}
		},
	}

	# Стратегия 5: Android Testsuite клиент
	ydl_opts_android_testsuite = {
		**base_opts_no_cookies,
		'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
		'extractor_args': {
			'youtube': {
				'player_client': ['android_testsuite'],
			}
		},
	}

	# Стратегия 6: Media Connect клиент
	ydl_opts_mediaconnect = {
		**base_opts_no_cookies,
		'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
		'extractor_args': {
			'youtube': {
				'player_client': ['mediaconnect'],
			}
		},
	}

	# Стратегия 7: Android VR клиент
	ydl_opts_android_vr = {
		**base_opts_no_cookies,
		'format': 'best[height<=1080][ext=mp4]/best',
		'extractor_args': {
			'youtube': {
				'player_client': ['android_vr'],
			}
		},
	}

	# Стратегия 8: Android клиент с куками
	ydl_opts_android_cookies = {
		**base_opts_with_cookies,
		'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
		'extractor_args': {
			'youtube': {
				'player_client': ['android'],
			}
		},
	}

	# Пробуем разные стратегии
	strategies = [
		('Android Music client', ydl_opts_android_music),
		('Android SDK-less client', ydl_opts_android_sdkless),
		('iOS client (with cookies)', ydl_opts_ios_cookies),
		('Web Safari client (with cookies)', ydl_opts_web_safari),
		('Android Testsuite client', ydl_opts_android_testsuite),
		('Media Connect client', ydl_opts_mediaconnect),
		('Android VR client', ydl_opts_android_vr),
		('Android client (with cookies)', ydl_opts_android_cookies),
	]

	best_download = None
	best_height = 0

	for strategy_name, ydl_opts in strategies:
		print(f'{Colors.OKCYAN}Trying strategy: {strategy_name}{Colors.ENDC}')
		ydl = YoutubeDL(ydl_opts)

		try:
			print('Extracting info and downloading...')
			info = ydl.extract_info(url)

			# Выводим информацию о скачанном формате
			if 'requested_downloads' in info and info['requested_downloads']:
				downloaded_format = info['requested_downloads'][0]
				height = downloaded_format.get('height', 0)
				width = downloaded_format.get('width', 'unknown')
				format_id = downloaded_format.get('format_id', 'unknown')
				print(f'{Colors.OKGREEN}Downloaded format: {format_id}, resolution: {width}x{height}{Colors.ENDC}')

				video_path = downloaded_format['filepath']
				filename = downloaded_format['filename'].replace(
					'D:\\Artyom\\Проекты\\Top Club Chart\\клипы чарта\\regulars\\', '')

				result = {
					'video_path': video_path,
					'filename': filename,
					'height': height,
					'width': width,
					'format_id': format_id,
				}

				# Проверяем качество
				if height >= min_height:
					print(f'{Colors.OKGREEN}✓ Quality check passed: {height}p >= {min_height}p{Colors.ENDC}')
					print(f'{Colors.OKGREEN}Successfully downloaded with {strategy_name}{Colors.ENDC}')
					return result
				else:
					print(f'{Colors.WARNING}Quality {height}p is lower than required {min_height}p, trying next strategy...{Colors.ENDC}')
					# Сохраняем как лучший вариант, если это лучше предыдущего
					if height > best_height:
						best_height = height
						best_download = result
					continue

		except ExtractorError as e:
			error_msg = str(e)
			print(f'{Colors.WARNING}Strategy "{strategy_name}" failed: {error_msg}{Colors.ENDC}')

			# Если формат недоступен, пробуем упрощённые варианты для этой стратегии
			if 'Requested format is not available' in error_msg or 'not available' in error_msg.lower():
				print(f'{Colors.WARNING}Trying fallback formats for {strategy_name}...{Colors.ENDC}')

				# Фоллбэки с приоритетом на высокое разрешение
				fallback_formats = [
					'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/best[height=1080]',
					'bestvideo[height=720][ext=mp4]+bestaudio[ext=m4a]/best[height=720]',
					'best[height<=1080]',
					'bestvideo+bestaudio/best',
				]

				for fallback_format in fallback_formats:
					try:
						print(f'{Colors.OKCYAN}  Trying format: {fallback_format}{Colors.ENDC}')
						ydl_opts_fallback = ydl_opts.copy()
						ydl_opts_fallback['format'] = fallback_format
						ydl = YoutubeDL(ydl_opts_fallback)
						info = ydl.extract_info(url)

						if 'requested_downloads' in info and info['requested_downloads']:
							downloaded_format = info['requested_downloads'][0]
							height = downloaded_format.get('height', 0)
							width = downloaded_format.get('width', 'unknown')
							format_id = downloaded_format.get('format_id', 'unknown')
							print(f'{Colors.OKGREEN}Downloaded format: {format_id}, resolution: {width}x{height}{Colors.ENDC}')

							video_path = downloaded_format['filepath']
							filename = downloaded_format['filename'].replace(
								'D:\\Artyom\\Проекты\\Top Club Chart\\клипы чарта\\regulars\\', '')

							result = {
								'video_path': video_path,
								'filename': filename,
								'height': height,
								'width': width,
								'format_id': format_id,
							}

							if height >= min_height:
								print(f'{Colors.OKGREEN}✓ Quality check passed: {height}p >= {min_height}p{Colors.ENDC}')
								print(f'{Colors.OKGREEN}Successfully downloaded with format: {fallback_format}{Colors.ENDC}')
								return result
							elif height > best_height:
								best_height = height
								best_download = result

					except Exception as fallback_error:
						print(f'{Colors.WARNING}  Format {fallback_format} failed: {fallback_error}{Colors.ENDC}')
						continue
			
			# Переходим к следующей стратегии
			continue
		except Exception as e:
			print(f'{Colors.WARNING}Strategy "{strategy_name}" failed with unexpected error: {e}{Colors.ENDC}')
			continue

	# Если мы нашли хотя бы какое-то видео, но оно ниже требуемого качества
	if best_download:
		print(f'{Colors.WARNING}⚠ Could not find video with {min_height}p or higher quality{Colors.ENDC}')
		print(f'{Colors.WARNING}Best available quality: {best_height}p{Colors.ENDC}')
		print(f'{Colors.WARNING}This may be due to YouTube restrictions. The video will be downloaded in {best_height}p.{Colors.ENDC}')
		return best_download

	# Если все стратегии не сработали
	print(f'{Colors.FAIL}All download strategies failed.{Colors.ENDC}')
	print(f'{Colors.FAIL}Please check:')
	print(f'{Colors.FAIL}  1. Video URL is correct and accessible')
	print(f'{Colors.FAIL}  2. yt-dlp is up to date (run: pip install -U yt-dlp)')
	print(f'{Colors.FAIL}  3. Video is not age-restricted or geo-blocked')
	print(f'{Colors.FAIL}  4. Check if cookies file exists: yt_cookies.txt{Colors.ENDC}')

	raise ExtractorError(f'Could not download video. All strategies and formats failed.')

def fill_file(songId: int, ytUrl: str):
	result = download_clip(ytUrl)
	video_path = result['video_path']
	analyze_result = ChorusFinder().analyze_track(video_path)
	print(analyze_result)

	song = song_repository.get_song_by_id(songId)
	song \
		.set_clip_name(result['filename']) \
		.set_clip_start_sec(analyze_result['start_times']) \
		.set_clip_end_sec(analyze_result['end_times']) \
		.save()


def fill_songs_with_no_clip():
	songs = song_repository.get_songs_with_no_clips()
	print(f'{Colors.OKCYAN}Found {len(songs)} songs without clips{Colors.ENDC}')
	for song in songs:
		print(f'{Colors.OKBLUE}Downloading clip for {song.id} {song.authors} - {song.name}{Colors.ENDC}')
		search_query = f'{song.authors} - {song.name}'
		yt_clip_id = find_clip(search_query)
		if not yt_clip_id:
			print(f'{Colors.WARNING}Skipping song {song.id} - no clip found{Colors.ENDC}')
			continue
		# yt_clip_id = 'ig9TBmz03Dg'
		yt_clip_url = f'https://www.youtube.com/watch?v={yt_clip_id}'
		fill_file(song.id, yt_clip_url)


def fill_songs_by_ids(song_ids: list):
	songs = [song_repository.get_song_by_id(song_id) for song_id in song_ids]
	for song in songs:
		print(f'{Colors.OKBLUE}Downloading clip for {song.id} {song.authors} - {song.name}{Colors.ENDC}')
		search_query = f'{song.authors} - {song.name}'
		yt_clip_id = find_clip(search_query)
		if not yt_clip_id:
			print(f'{Colors.WARNING}Skipping song {song.id} - no clip found{Colors.ENDC}')
			continue
		# yt_clip_id = 'ig9TBmz03Dg'
		yt_clip_url = f'https://www.youtube.com/watch?v={yt_clip_id}'
		fill_file(song.id, yt_clip_url)


def fill_concrete_song(song_id: int, yt_id: str):
	print(f'{Colors.OKBLUE}Downloading clip for {song_id}{Colors.ENDC}')
	yt_clip_url = f'https://www.youtube.com/watch?v={yt_id}'
	fill_file(song_id, yt_clip_url)


def just_download(yt_id: str):
	yt_clip_url = f'https://www.youtube.com/watch?v={yt_id}'
	result = download_clip(yt_clip_url)
	print(result)

# Run script - D:\Artyom\Проекты\Python\tcc-render\venv\Scripts\python.exe D:\Artyom\Проекты\Python\tcc-render\yt_clip_downloader.py


if __name__ == '__main__':
	fill_concrete_song(577, 'M07nvkbQFzI')
	# just_download('ovznTayG7FQ')
	# fill_songs_with_no_clip()
	# fill_songs_by_ids([260])
