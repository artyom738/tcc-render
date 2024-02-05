import MySQLdb

import database


class Song:
	def __init__(self, data):
		self.id = data.get('id')
		self.name = data.get('name')
		self.authors = data.get('authors')
		self.ep_id = data.get('ep_id')
		self.original_id = data.get('original_id')
		self.clip_path = data.get('clip_path')
		self.clip_start_sec = data.get('clip_start_sec')
		self.clip_end_sec = data.get('clip_end_sec')

	# region Setters
	def set_id(self, song_id):
		self.id = song_id

		return self

	def set_name(self, name):
		self.name = name

		return self

	def set_authors(self, authors):
		self.authors = authors

		return self

	def set_ep_id(self, ep_id):
		self.ep_id = ep_id

		return self

	# endregion

	def get_peak(self):
		query = 'select MIN(POSITION) as peak from charts where SONG_ID = ' + str(int(self.id))
		result = database.get_list(query)
		min_position = result[0]['peak']

		query = 'select COUNT(*) as peak_times from charts where SONG_ID = %s AND POSITION = %s'
		result = database.get_list(query, (self.id, min_position))
		peak_times = result[0]['peak_times']

		if peak_times > 1:
			return str(min_position) + '(' + str(peak_times) + ')'
		else:
			return str(min_position)

	def get_weeks(self):
		query = 'select count(*) as weeks from charts where SONG_ID = ' + str(self.id)
		result = database.get_list(query)

		return result[0]['weeks']

	def save(self):
		if self.id is None:
			query = "insert into songs (EP_ID, AUTHORS, NAME, CLIP_PATH, CLIP_START_SEC, CLIP_END_SEC) " \
				"values (%s, %s, %s, %s, %s, %s)"
			result = database.add(query, (
				self.ep_id or 0,
				self.authors or '',
				self.name or '',
				self.clip_path or '',
				self.clip_start_sec or 0,
				self.clip_end_sec or 0
			))
			self.set_id(result)
		else:
			query = "update songs set EP_ID = %s, AUTHORS = %s, NAME = %s, CLIP_PATH = %s, CLIP_START_SEC = %s, CLIP_END_SEC = %s where songs.ID = %s"
			result = database.add(query, (
				self.ep_id or 0,
				self.authors or '',
				self.name or '',
				self.clip_path or '',
				self.clip_start_sec or 0,
				self.clip_end_sec or 0,
				self.id
			))

		return self
