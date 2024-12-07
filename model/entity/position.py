from datetime import datetime, timedelta

import database
from model.repository.chart_repository import chart_repository


class Position:
	def __init__(self, data):
		self.position = data.get('position')
		self.song_id = data.get('song_id')
		self.chart_id = data.get('chart_id')
		self.moving = None
		self.is_lcs = False

	def save(self):
		query = "insert into chart_positions (CHART_ID, SONG_ID, POSITION) values (%s, %s, %s)"
		result = database.add(query, (
			self.chart_id or 0,
			self.song_id or '',
			self.position or 0
		))

		return self

	def get_lw(self):
		previous_chart = chart_repository.get_previous_chart(self.chart_id)
		if not previous_chart:
			return None

		query = f'select cp.POSITION from chart_positions cp where cp.SONG_ID = {self.song_id} AND cp.CHART_ID = {previous_chart.id}'
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
		elif lw is None:
			return None
		elif int(lw) == self.position:
			return 'same'
		elif int(lw) > self.position:
			return 'up'
		elif int(lw) < self.position:
			return 'down'
