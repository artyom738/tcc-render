from datetime import datetime, timedelta

import database


class Position:
	def __init__(self, data):
		self.position = data.get('position')
		self.song_id = data.get('song_id')
		self.chart_date = data.get('chart_date')
		self.chart_type = data.get('chart_type')
		self.moving = None
		self.is_lcs = False

	def save(self):
		query = "insert into charts (CHART_DATE, SONG_ID, POSITION, CHART_TYPE) values (%s, %s, %s, %s)"
		result = database.add(query, (
			self.chart_date or '',
			self.song_id or '',
			self.position or 0,
			self.chart_type or '',
		))

		return self

	def get_lw(self):
		prev_date = self.chart_date - timedelta(days=7)
		str_prev_date = datetime.strftime(prev_date, '%Y-%m-%d')
		# str_prev_date = '2023-12-23'
		query = f'select POSITION from charts where SONG_ID = {self.song_id} AND CHART_DATE = {str_prev_date} AND CHART_TYPE = {self.chart_type}'
		result = database.get_list(query)
		if len(result) < 1:
			return '--'
		else:
			return result[0]['POSITION']

	def get_moving(self):
		if self.moving is not None:
			return self.moving

		lw = self.get_lw()
		if lw == '--':
			return 'new'
		elif int(lw) == self.position:
			return 'same'
		elif int(lw) > self.position:
			return 'up'
		elif int(lw) < self.position:
			return 'down'
