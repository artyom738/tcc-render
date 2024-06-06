import requests

from connectors.base_connector import BaseConnector
from model.entity.chart import Chart
from model.entity.position import Position
from model.entity.song import Song
from model.repository.position_repository import position_repository
from model.repository.song_repository import song_repository


class EuropaPlusConnector(BaseConnector):
	def get_data(self, chart: Chart) -> list:
		api_url = self.get_api_url(chart)
		response = requests.get(api_url)
		res = response.json()
		return res['data']

	def save_positions(self, chart: Chart, data: list) -> None:
		if data:
			for song in data:
				ep_id = song['id']
				position = song['hit_data']['place']
				song_object = song_repository.get_song_by_ep_id(ep_id)
				if not song_object:
					artists = song['artists']
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
		raise NotImplementedError

	def save_rubrics(self, chart_id: int, rubrics: dict):
		raise NotImplementedError
