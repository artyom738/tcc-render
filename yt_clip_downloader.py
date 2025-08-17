import os

from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

from chorus_finder.finder import ChorusFinder
from terminal_colors import Colors

import chorus_finder
from model.repository.song_repository import song_repository


def find_clip(query, max_results=10):
	videos_search = VideosSearch(query, limit=max_results)
	results = videos_search.result()
	for song in results['result']:
		if song['channel']['name'] == 'Selected':
			continue
		else:
			return song['id']

	return results['result'][0]['id']


def download_clip(url: str):
	ydl_opts = {
		'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]',
		'keepvideo': False,
		'outtmpl': 'D:/Artyom/Проекты/Top Club Chart/клипы чарта/regulars/%(title)s.%(ext)s',
		'cookiefile': 'yt_cookies.txt'
	}

	ydl = YoutubeDL(ydl_opts)

	try:
		info = ydl.extract_info(url)
	except Exception:
		print(f'{Colors.FAIL}Format 137+140 is not available. Trying maximum resolution below 1080p with any audio.{Colors.ENDC}')
		ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]'
		ydl = YoutubeDL(ydl_opts)
		info = ydl.extract_info(url)

	video_path = info['requested_downloads'][0]['filepath']
	ydl.download([url])

	return {
		'video_path': video_path,
		'filename': info['requested_downloads'][0]['filename'].replace(
			'D:\\Artyom\\Проекты\\Top Club Chart\\клипы чарта\\regulars\\', ''),
	}


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
		# yt_clip_id = 'ig9TBmz03Dg'
		yt_clip_url = f'https://www.youtube.com/watch?v={yt_clip_id}'
		fill_file(song.id, yt_clip_url)


def fill_songs_by_ids(song_ids: list):
	songs = [song_repository.get_song_by_id(song_id) for song_id in song_ids]
	for song in songs:
		print(f'{Colors.OKBLUE}Downloading clip for {song.id} {song.authors} - {song.name}{Colors.ENDC}')
		search_query = f'{song.authors} - {song.name}'
		yt_clip_id = find_clip(search_query)
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


if __name__ == '__main__':
	fill_concrete_song(1404, 'tZ192uMAPRA')
	# just_download('4zb7p3GG2Ig')
	# fill_songs_with_no_clip()
	# fill_songs_by_ids([260])

