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
		json_data = '''
[{"position": 1, "artists": "Seeb", "title": "Before You Go", "external_id": "dht50"},{"position": 2, "artists": "Madison Beer", "title": "Make You Mine", "external_id": "dht28"},{"position": 3, "artists": "Jaxomy, Agatino Romero & Raffaella Carrà", "title": "Pedro", "external_id": "dht77"},{"position": 4, "artists": "Zerb & The Chainsmokers feat. Ink", "title": "Addicted", "external_id": "dht71"},{"position": 5, "artists": "Armin van Buuren & Gryffin", "title": "What Took You So Long", "external_id": "dht70"},{"position": 6, "artists": "Robin Schulz & Topic feat. Oaks", "title": "One By One", "external_id": "dht12"},{"position": 7, "artists": "Kygo & Ava Max", "title": "Whatever", "external_id": "dht3"},{"position": 8, "artists": "Leony", "title": "Simple Life", "external_id": "dht59"},{"position": 9, "artists": "Calvin Harris & Rag'n'Bone Man", "title": "Lovers In A Past Life", "external_id": "dht24"},{"position": 10, "artists": "TDJ", "title": "Come Back Home", "external_id": "dht55"},{"position": 11, "artists": "Lufthaus & Robbie Williams feat. Sophie Ellis-Bextor ", "title": "Immortal", "external_id": "dht5"},{"position": 12, "artists": "Alok & Bebe Rexha", "title": "Deep In Your Love", "external_id": "dht6"},{"position": 13, "artists": "Alan Walker & Daya", "title": "Heart Over Mind", "external_id": "dht1"},{"position": 14, "artists": "Lucas Estrada, Tribbs & Stephen Puth", "title": "Close Your Eyes", "external_id": "dht45"},{"position": 15, "artists": "John Summit & Hayla", "title": "Shiver", "external_id": "dht36"},{"position": 16, "artists": "Nero", "title": "Blame You", "external_id": "dht25"},{"position": 17, "artists": "Maggie Lindemann", "title": "Hostage", "external_id": "dht17"},{"position": 18, "artists": "DVRST & polnalyubvi", "title": "Falling Stars", "external_id": "dht67"},{"position": 19, "artists": "David Guetta & OneRepublic", "title": "I Don't Wanna Wait", "external_id": "dht79"},{"position": 20, "artists": "INJI", "title": "BIG UP", "external_id": "dht84"},{"position": 21, "artists": "Tiësto, Dimitri Vegas & Like Mike, Gabry Ponte", "title": "Mockingbird", "external_id": "dht75"},{"position": 22, "artists": "The Knocks & Sofi Tukker", "title": "One On One", "external_id": "dht10"},{"position": 23, "artists": "Eliza Rose & Calvin Harris", "title": "Body Moving", "external_id": "dht7"},{"position": 24, "artists": "Jhay Rivas", "title": "SAFE WITH ME (SECRETOS)", "external_id": "dht76"},{"position": 25, "artists": "Delta Heavy & Cameron Warren", "title": "Bad Decisions", "external_id": "dht82"},{"position": 26, "artists": "Jax Jones & Zoe Wees", "title": "Never Be Lonely", "external_id": "dht23"},{"position": 27, "artists": "Alle Farben & Maurice Lessing feat. Emma Wells", "title": "Dreams", "external_id": "dht51"},{"position": 28, "artists": "Dagny", "title": "Strawberry Dream", "external_id": "dht80"},{"position": 29, "artists": "Marshmello, P!nk & Sting", "title": "Dreaming", "external_id": "dht4"},{"position": 30, "artists": "Hayla", "title": "Embers", "external_id": "dht83"},{"position": 31, "artists": "Third ≡ Party", "title": "Believe", "external_id": "dht90"},{"position": 32, "artists": "AURORA", "title": "Your Blood", "external_id": "dht8"},{"position": 33, "artists": "Kris Kross Amsterdam & INNA", "title": "Queen of My Castle", "external_id": "dht88"},{"position": 34, "artists": "Armin van Buuren & Goodboys", "title": "Forever (Stay Like This)", "external_id": "dht15"},{"position": 35, "artists": "GAMPER & DADONI feat. Becky Smith", "title": "Your Symphony", "external_id": "dht89"},{"position": 36, "artists": "Campbell & Alcemist", "title": "Would You (go to bed with me)", "external_id": "dht69"},{"position": 37, "artists": "Heidi Klum", "title": "Sunglasses at Night", "external_id": "dht56"},{"position": 38, "artists": "twocolors & Roe Byrne", "title": "Stereo", "external_id": "dht87"},{"position": 39, "artists": "Mau P", "title": "Beats For The Underground", "external_id": "dht14"},{"position": 40, "artists": "Galantis, David Guetta & 5 Seconds of Summer", "title": "Lighter", "external_id": "dht53"},{"position": 41, "artists": "тринадцать карат", "title": "Саша, останься со мной", "external_id": "dht85"},{"position": 42, "artists": "Felix Jaehn feat. Jasmine Thompson", "title": "Without You", "external_id": "dht94"},{"position": 43, "artists": "Mau P", "title": "On Again", "external_id": "dht86"},{"position": 44, "artists": "Martin Garrix & Third Party feat. Oaks & Declan J Donovan", "title": "Carry You", "external_id": "dht31"},{"position": 45, "artists": "Don Diablo", "title": "Smalltown Boy", "external_id": "dht93"},{"position": 46, "artists": "Olivia Rodrigo", "title": "obsessed", "external_id": "dht68"},{"position": 47, "artists": "Dimitri Vegas & Like Mike, Tiësto, W&W feat. Dido", "title": "Thank You (Not So Bad)", "external_id": "dht22"},{"position": 48, "artists": "Kenya Grace", "title": "It's Not Fair", "external_id": "dht63"},{"position": 49, "artists": "MEDUZA, OneRepublic & Leony", "title": "Fire (Official UEFA EURO 2024 Song)", "external_id": "dht92"},{"position": 50, "artists": "Stand Atlantic", "title": "LOVE U ANYWAY", "external_id": "dht91"}]
		'''
		return json.loads(json_data)

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
		'chart_number': 12,
		'chart_date': '2024-05-18',
		'chart_type': 'dark',
	}).save()
	connector = DarkConnector()
	connector.save_chart_data(chart)
