from datetime import datetime, date

import requests

from connectors.base_connector import BaseConnector
from model.entity.chart import Chart
from model.entity.position import Position
from model.entity.song import Song
from model.repository.position_repository import position_repository
from model.repository.song_repository import song_repository


class TccNewYearConnector(BaseConnector):
	def get_data(self, chart: Chart) -> list:
		api_url = self.get_api_url(chart)
		response = requests.get(api_url)
		res = response.json()
		return res['data']

	def save_positions(self, chart: Chart, data: dict) -> None:
		if data:
			for position_item in data['chart']['items']:
				song = position_item['song']
				ep_id = song['id']
				position = position_item['position']
				song_object = song_repository.get_song_by_ep_id(ep_id)
				if not song_object:
					print(position_item)
					artists = song['singers']
					db_authors = ''
					if artists:
						db_authors = ' & '.join([artist['artist'] for artist in artists])
					name = song['name']
					song_object = Song({
						'name': name,
						'authors': db_authors,
						'ep_id': ep_id or 0,
					}).save()
				position_object = position_repository.get_position_in_chart(song_object.id, chart.id)
				if position_object is None:
					Position({
						'position': position,
						'song_id': song_object.id,
						'chart_id': chart.id,
					}).save()

	def get_api_url(self, chart: Chart):
		return 'https://admin.europaplus.ru/api/year-club-chart?year=2024&region=1'

	def save_rubrics(self, chart_id: int, rubrics: dict):
		return None

	def get_chart_type(self) -> str:
		return 'tcc_ny'

	def get_last_chart_date(self) -> date:
		return datetime.strptime('2024-12-31', '%Y-%m-%d').date()

	def save_rubrics(self, chart_id: int, rubrics: dict):
		return None
