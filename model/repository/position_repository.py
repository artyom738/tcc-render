import database
from datetime import datetime, timedelta
from model.entity.position import Position


class PositionRepository:
	def __init__(self):
		pass

	def get_position_by_song_and_date(self, song_id: int, date: datetime):
		str_date = date.strftime("%Y-%m-%d")
		query = 'select * from charts c where SONG_ID = %s and CHART_DATE = %s'
		result = database.get_list(query, (song_id, str_date))

		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def get_positions_by_date(self, date: datetime):
		str_date = date.strftime("%Y-%m-%d")
		query = "select * from charts c where CHART_DATE = '" + str_date + "' and POSITION < 300 and POSITION > 0 order by POSITION desc"
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
		query = "select SONG_ID from charts c where CHART_DATE = '" + prev_date + "' order by POSITION desc"
		prev_songs = []
		db_result = database.get_list(query)
		if len(db_result) > 0:
			for position in db_result:
				prev_songs.append(position['SONG_ID'])

		current_songs = []
		query = "select SONG_ID from charts c where CHART_DATE = '" + date.strftime('%Y-%m-%d') + "' order by POSITION desc"
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
				}))

		return outs

	def fetch_object(self, data: dict) -> Position:
		return Position({
			'chart_date': data['CHART_DATE'],
			'song_id': data['SONG_ID'],
			'position': data['POSITION'],
		})
