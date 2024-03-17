import random
import database


class Song:
	def __init__(self, data):
		clip_start_sec = []
		if data.get('clip_start_sec'):
			clip_start_sec = [float(item) for item in str(data.get('clip_start_sec')).split(',')]

		clip_end_sec = []
		if data.get('clip_end_sec'):
			clip_end_sec = [float(item) for item in str(data.get('clip_end_sec')).split(',')]

		self.id: int = data.get('id')
		self.name: str = data.get('name')
		self.authors: str = data.get('authors')
		self.ep_id: int = data.get('ep_id')
		self.original_id: int = data.get('original_id')
		self.clip_path: str = data.get('clip_path')
		self.clip_name: str = data.get('clip_name')
		self.clip_start_sec: list[float] = clip_start_sec
		self.clip_end_sec: list[float] = clip_end_sec

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

	def set_clip_path(self, clip_path):
		self.clip_path = clip_path

		return self

	def set_clip_name(self, clip_name):
		self.clip_name = clip_name

		return self

	def set_clip_start_sec(self, clip_start_sec: list[float]):
		self.clip_start_sec = clip_start_sec

		return self

	def set_clip_end_sec(self, clip_end_sec: list[float]):
		self.clip_end_sec = clip_end_sec

		return self

	def get_clip_times(self):
		start_times = self.clip_start_sec
		random_index = random.randint(0, len(start_times) - 1)

		return {
			'start_time': float(start_times[random_index]),
			'end_time': float(self.clip_end_sec[random_index]),
		}
	# endregion

	def get_peak(self, chart_type: str):
		query = f'select MIN(POSITION) as peak from charts where SONG_ID = {str(self.id)} and CHART_TYPE = \'{chart_type}\''
		result = database.get_list(query)
		min_position = result[0]['peak']

		query = f'select COUNT(*) as peak_times from charts where SONG_ID = {self.id} AND POSITION = {min_position} and CHART_TYPE = \'{chart_type}\''
		result = database.get_list(query)
		peak_times = result[0]['peak_times']

		if peak_times > 1:
			return str(min_position) + '(' + str(peak_times) + ')'
		else:
			return str(min_position)

	def get_weeks(self, chart_type: str):
		query = f'select count(*) as weeks from charts where SONG_ID = {str(self.id)} and CHART_TYPE = \'{chart_type}\''
		result = database.get_list(query)

		return result[0]['weeks']

	def save(self):
		if self.id is None:
			query = "insert into songs (EP_ID, AUTHORS, NAME, CLIP_PATH, CLIP_START_SEC, CLIP_END_SEC) " \
				"values (%s, %s, %s, %s, %s, %s)"
			clip_start_sec = list(self.clip_start_sec or [])
			clip_end_sec = list(self.clip_end_sec or [])
			result = database.add(query, (
				self.ep_id or 0,
				self.authors or '',
				self.name or '',
				self.clip_name or '',
				','.join(str(v) for v in clip_start_sec),
				','.join(str(v) for v in clip_end_sec),
			))
			self.set_id(result)
		else:
			query = "update songs set EP_ID = %s, AUTHORS = %s, NAME = %s, CLIP_PATH = %s, CLIP_START_SEC = %s, CLIP_END_SEC = %s where songs.ID = %s"
			clip_start_sec = list(self.clip_start_sec or [])
			clip_end_sec = list(self.clip_end_sec or [])
			result = database.add(query, (
				self.ep_id or 0,
				self.authors or '',
				self.name or '',
				self.clip_name or '',
				','.join(str(v) for v in clip_start_sec),
				','.join(str(v) for v in clip_end_sec),
				self.id
			))

		return self
