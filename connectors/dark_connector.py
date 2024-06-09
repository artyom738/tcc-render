import json
from datetime import datetime, timedelta, date

from connectors.base_connector import BaseConnector
from model.entity.chart import Chart
from model.entity.position import Position
from model.entity.song import Song
from model.repository.position_repository import position_repository
from model.repository.song_repository import song_repository


class DarkConnector(BaseConnector):
	def get_data(self, chart: Chart) -> list:
		json_data = open('dark.json')
		return json.load(json_data)

	def get_chart_type(self) -> str:
		return 'dark'

	def get_last_chart_date(self) -> date:
		today = datetime.today()
		weekday = today.weekday()
		days_to_last_saturday = (weekday - 5) % 7  # 5 matches saturday
		last_saturday = today - timedelta(days=days_to_last_saturday)
		return last_saturday.date()

	def save_positions(self, chart: Chart, data: list):
		for song in data:
			external_id = song['external_id']
			position = song['position']
			song_object = song_repository.get_song_by_ep_id(external_id)
			if not song_object:
				artists = song['artists']
				name = song['title']
				song_object = Song({
					'name': name,
					'authors': artists,
					'ep_id': external_id,
				}).save()
			position_object = position_repository.get_position_in_chart(song_object.id, chart.id)
			if position_object is None:
				Position({
					'position': position,
					'song_id': song_object.id,
					'chart_id': chart.id,
				}).save()


if __name__ == '__main__':
	chart = Chart({
		'id': None,
		'chart_number': 14,
		'chart_date': '2024-06-01',
		'chart_type': 'dark',
	}).save()
	connector = DarkConnector()
	connector.save_chart_data(chart)
