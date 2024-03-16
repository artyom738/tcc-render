import os

from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from terminal_colors import Colors

import chorus_finder
from model.repository.song_repository import SongRepository


def find_clip(query, max_results=1):
	videos_search = VideosSearch(query, limit=max_results)
	results = videos_search.result()

	return results['result'][0]['id']


def download_clip(url: str):
	ydl_opts = {
		'format': '137+140',
		'keepvideo': True,
		'outtmpl': 'D:/Artyom/Проекты/Top Club Chart/клипы чарта/regulars/%(title)s.%(ext)s',
	}

	ydl = YoutubeDL(ydl_opts)

	try:
		info = ydl.extract_info(url)
	except Exception:
		print(f'{Colors.FAIL}Format 137+140 is not available{Colors.ENDC}')
		ydl_opts.pop('format')
		ydl = YoutubeDL(ydl_opts)
		info = ydl.extract_info(url)

	video_path = info['requested_downloads'][0]['__files_to_merge'][0]
	audio_path = info['requested_downloads'][0]['__files_to_merge'][1]
	ydl.download([url])

	return {
		'video_path': video_path,
		'audio_path': audio_path,
		'filename': info['requested_downloads'][0]['filename'].replace(
			'D:\\Artyom\\Проекты\\Top Club Chart\\клипы чарта\\regulars\\', ''),
	}


def fill_file(songId: int, ytUrl: str):
	result = download_clip(ytUrl)
	audio_file = result['audio_path']
	analyze_result = chorus_finder.analyze_track(audio_file)
	print(analyze_result)
	os.remove(result['video_path'])
	os.remove(result['audio_path'])

	song = SongRepository().get_song_by_id(songId)
	song \
		.set_clip_path(result['filename']) \
		.set_clip_start_sec(analyze_result['start_times']) \
		.set_clip_end_sec(analyze_result['end_times']) \
		.save()


def fill_songs_with_no_clip():
	songs = SongRepository().get_songs_with_no_clips()
	print(f'{Colors.OKCYAN}Found {len(songs)} songs without clips{Colors.ENDC}')
	for song in songs:
		print(f'{Colors.OKBLUE}Downloading clip for {song.id} {song.authors} - {song.name}{Colors.ENDC}')
		search_query = f'{song.authors} - {song.name} official music video -selected'  # For not to use boring clips from Selected channel
		yt_clip_id = find_clip(search_query)
		# yt_clip_id = 'ig9TBmz03Dg'
		yt_clip_url = f'https://www.youtube.com/watch?v={yt_clip_id}'
		fill_file(song.id, yt_clip_url)


def fill_concrete_song(song_id: int, yt_id: str):
	print(f'{Colors.OKBLUE}Downloading clip for {song_id}{Colors.ENDC}')
	yt_clip_url = f'https://www.youtube.com/watch?v={yt_id}'
	fill_file(song_id, yt_clip_url)


if __name__ == '__main__':
	fill_songs_with_no_clip()
	# fill_concrete_song(473, 'RlsJr2V8afo')
	# fill_concrete_song(474, 'DEi_z08bcro')
