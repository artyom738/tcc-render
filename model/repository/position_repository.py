import database
from datetime import datetime, timedelta
from model.entity.position import Position


class PositionRepository:
	def __init__(self, chart_type: str):
		self.chart_type: str = chart_type

	def get_position_by_song_and_date(self, song_id: int, date: datetime):
		query = f'select * from charts c where SONG_ID = {str(song_id)} and CHART_DATE = \'{date.strftime("%Y-%m-%d")}\' and CHART_TYPE = \'{self.chart_type}\''
		result = database.get_list(query)

		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def get_positions_by_date(self, date: datetime):
		query = f'select * from charts c where CHART_DATE = \'{date.strftime("%Y-%m-%d")}\' and POSITION < 300 and POSITION > 0 and CHART_TYPE = \'{self.chart_type}\' order by POSITION desc'
		db_result = database.get_list(query)
		result = []
		if len(db_result) > 0:
			for position in db_result:
				result.append(self.fetch_object(position))
			return result
		else:
			return []

	def get_outs_by_date(self, date: datetime):
		prev_date = date - timedelta(days=7)
		prev_date = prev_date.strftime('%Y-%m-%d')
		# prev_date = '2023-12-23'
		query = f'select SONG_ID from charts c where CHART_DATE = \'{prev_date}\' and CHART_TYPE = \'{self.chart_type}\' order by POSITION desc'
		prev_songs = []
		db_result = database.get_list(query)
		if len(db_result) > 0:
			for position in db_result:
				prev_songs.append(position['SONG_ID'])

		current_songs = []
		query = f'select SONG_ID from charts c where CHART_DATE = \'{date.strftime("%Y-%m-%d")}\' and CHART_TYPE = \'{self.chart_type}\' order by POSITION desc'
		db_result = database.get_list(query)
		if len(db_result) > 0:
			for position in db_result:
				current_songs.append(position['SONG_ID'])

		outs = []
		for position in prev_songs:
			if position not in current_songs:
				outs.append(self.fetch_object({
					'CHART_DATE': date,
					'SONG_ID': position,
					'POSITION': 99,
					'CHART_TYPE': self.chart_type,
				}))

		return outs

	def fetch_object(self, data: dict) -> Position:
		return Position({
			'chart_date': data['CHART_DATE'],
			'song_id': data['SONG_ID'],
			'position': data['POSITION'],
			'chart_type': data['CHART_TYPE'],
		})
