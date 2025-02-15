import random
from datetime import datetime

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
		self.ep_id: str = data.get('ep_id')
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
	# endregion

	def get_clip_times(self):
		start_times = self.clip_start_sec
		if len(start_times) == 0:
			raise ValueError(f'Song {self.id} {self.authors} - {self.name} has no start times')

		if len(start_times) == 1:
			return {
				'start_time': float(start_times[0]),
				'end_time': float(self.clip_end_sec[0]),
			}

		random_index = random.randint(0, len(start_times) - 1)

		return {
			'start_time': float(start_times[random_index]),
			'end_time': float(self.clip_end_sec[random_index]),
		}

	def get_peak(self, chart_type: str, chart_date: datetime = None):
		# chart_type = 'tcc'
		# chart_date = None
		query = f'select MIN(cp.POSITION) as peak from chart_positions cp left join charts c on c.ID = cp.CHART_ID where cp.SONG_ID = {str(self.id)} and c.CHART_TYPE = \'{chart_type}\''
		if chart_date:
			query += f' and c.CHART_DATE <= \'{chart_date.strftime("%Y-%m-%d")}\' and c.CHART_DATE > "2024-01-01"'
		result = database.get_list(query)
		min_position = result[0]['peak']
		if not min_position:
			return '--'

		query = f'select COUNT(*) as peak_times from chart_positions cp left join charts c on c.ID = cp.CHART_ID where cp.SONG_ID = {self.id} AND cp.POSITION = {min_position} and c.CHART_TYPE = \'{chart_type}\''
		if chart_date:
			query += f' and c.CHART_DATE <= \'{chart_date.strftime("%Y-%m-%d")}\' and c.CHART_DATE > "2024-01-01"'
		result = database.get_list(query)
		peak_times = result[0]['peak_times']

		if peak_times > 1:
			return str(min_position) + '(' + str(peak_times) + ')'
		else:
			return str(min_position)

	def get_weeks(self, chart_type: str, chart_date: datetime = None):
		# chart_type = 'tcc'
		# chart_date = None
		query = f'select count(*) as weeks from chart_positions cp left join charts c on c.ID = cp.CHART_ID where cp.SONG_ID = {self.id} and c.CHART_TYPE = \'{chart_type}\''
		if chart_date:
			query += f' and c.CHART_DATE <= \'{chart_date.strftime("%Y-%m-%d")}\' and c.CHART_DATE > "2024-01-01"'
		result = database.get_list(query)

		return result[0]['weeks']

	def get_charts(self, chart_type: str):
		# chart_type = 'eht'
		query = f'select cp.POSITION, c.CHART_DATE from chart_positions cp left join charts c on c.ID = cp.CHART_ID where cp.SONG_ID = {self.id} and c.CHART_TYPE = \'{chart_type}\' order by c.CHART_DATE'
		result = database.get_list(query)

		return result

	def get_points(self, chart_type: str, date_start: datetime, date_end: datetime):
		max_points = 41
		if chart_type == 'eht':
			max_points = 41
		if chart_type == 'tcc':
			max_points = 26
		query = f'select sum({max_points}-cp.POSITION) as points from chart_positions cp left join charts c on c.ID = cp.CHART_ID where cp.SONG_ID = {self.id} and c.CHART_TYPE = \'{chart_type}\' and c.CHART_DATE > \'{date_start.strftime("%Y-%m-%d")}\' and c.CHART_DATE < \'{date_end.strftime("%Y-%m-%d")}\''
		result = database.get_list(query)

		return result[0]['points']

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
