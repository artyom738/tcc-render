from __future__ import annotations

import database
from model.entity.song import Song


class SongRepository:
	def __init__(self):
		pass

	def get_song_by_id(self, song_id) -> Song | None:
		query = 'select * from songs where ID = ' + str(int(song_id))
		result = database.get_list(query)

		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def get_song_by_ep_id(self, ep_id) -> Song | None:
		query = 'select * from songs where EP_ID = ' + str(int(ep_id))
		result = database.get_list(query)
		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def fetch_object(self, data) -> Song:
		return Song({
			'id': data['ID'],
			'name': data['NAME'],
			'authors': data['AUTHORS'],
			'ep_id': data['EP_ID'],
			'original_id': data['ORIGINAL_ID'],
			'clip_path': data['CLIP_PATH'],
			'clip_start_sec': data['CLIP_START_SEC'],
			'clip_end_sec': data['CLIP_END_SEC'],
		})
