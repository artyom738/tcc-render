from __future__ import annotations

import database
from model.entity.song import Song


class SongRepository:
	def __init__(self):
		pass

	def get_song_by_id(self, song_id) -> Song | None:
		query = f'select * from songs where ID = {str(int(song_id))}'
		result = database.get_list(query)

		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def get_song_by_ep_id(self, ep_id: str) -> Song | None:
		if ep_id == 0:
			return None
		query = f'select * from songs where EP_ID = \'{ep_id}\''
		result = database.get_list(query)
		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def get_songs_with_no_clips(self, min_id_filter=0) -> list[Song]:
		query = f'select * from songs where ID >= {str(int(min_id_filter))} and (CLIP_PATH is null or CLIP_PATH = \'\')'
		song_list = database.get_list(query)

		return [self.fetch_object(item) for item in song_list]

	def get_by_greater_id(self, min_id: int = 0):
		query = f'select * from songs where ID >= {str(min_id)}'
		song_list = database.get_list(query)

		return [self.fetch_object(item) for item in song_list]

	def fetch_object(self, data) -> Song:
		default_clip_path = 'D:/Artyom/Проекты/Top Club Chart/клипы чарта/regulars/'
		clip_path = ''
		if data['CLIP_PATH']:
			clip_path = default_clip_path + data['CLIP_PATH']

		return Song({
			'id': data['ID'],
			'name': data['NAME'],
			'authors': data['AUTHORS'],
			'ep_id': data['EP_ID'],
			'original_id': data['ORIGINAL_ID'],
			'clip_name': data['CLIP_PATH'],
			'clip_path': clip_path,
			'clip_start_sec': data['CLIP_START_SEC'],
			'clip_end_sec': data['CLIP_END_SEC'],
		})


song_repository = SongRepository()
