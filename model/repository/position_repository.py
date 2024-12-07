import database
from datetime import datetime, timedelta
from model.entity.position import Position
from model.repository.chart_repository import chart_repository


class PositionRepository:
	def __init__(self):
		pass

	def get_position_in_chart(self, song_id: int, chart_id: int):
		query = f'select * from chart_positions cp where cp.SONG_ID = {song_id} and cp.CHART_ID = {chart_id}'
		result = database.get_list(query)

		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def get_chart_positions(self, chart_id: int):
		query = f'select * from chart_positions cp where cp.CHART_ID = {chart_id} and cp.POSITION < 300 and cp.POSITION > 0 order by cp.POSITION desc'
		db_result = database.get_list(query)
		result = []
		if len(db_result) > 0:
			for position in db_result:
				result.append(self.fetch_object(position))
			return result
		else:
			return []

	def get_chart_outs(self, chart_id: int):
		previous_chart = chart_repository.get_previous_chart(chart_id)
		if not previous_chart:
			return []

		query = f'select SONG_ID from chart_positions cp where cp.CHART_ID = {previous_chart.id} order by cp.POSITION desc'
		prev_songs = []
		db_result = database.get_list(query)
		if len(db_result) > 0:
			for position in db_result:
				prev_songs.append(position['SONG_ID'])

		current_songs = []
		query = f'select SONG_ID from chart_positions cp where cp.CHART_ID = {chart_id} order by cp.POSITION desc'
		db_result = database.get_list(query)
		if len(db_result) > 0:
			for position in db_result:
				current_songs.append(position['SONG_ID'])

		outs = []
		for position in prev_songs:
			if position not in current_songs:
				outs.append(self.fetch_object({
					'SONG_ID': position,
					'POSITION': 99,
					'CHART_ID': chart_id,
				}))
		# outs.reverse()

		return outs

	def fetch_object(self, data: dict) -> Position:
		return Position({
			'chart_id': data['CHART_ID'],
			'song_id': data['SONG_ID'],
			'position': data['POSITION'],
		})


position_repository = PositionRepository()
