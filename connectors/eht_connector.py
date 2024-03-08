import requests

from datetime import datetime, timedelta
from model.entity.position import Position
from model.entity.song import Song
from model.repository.position_repository import PositionRepository
from model.repository.song_repository import SongRepository


def fill_db_chart(date: datetime):
	str_date = date_to_start.strftime("%Y-%m-%d")
	api_url = "https://europaplus.ru/api/programs/top40?date=" + str_date
	response = requests.get(api_url)
	res = response.json()
	chart_type = 'eht'

	data = res['data']
	if data:
		for song in data:
			ep_id = song['id']
			position = song['hit_data']['place']
			song_object = SongRepository().get_song_by_ep_id(ep_id)
			if not song_object:
				artists = song['artists']
				db_authors = ''
				if artists:
					db_authors = ' & '.join([artist['artist'] for artist in artists])
				name = song['name']
				song_object = Song({
					'name': name,
					'authors': db_authors,
					'ep_id': ep_id,
				})
				song_object = song_object.save()
			position_object = PositionRepository(chart_type).get_position_by_song_and_date(song_object.id, date)
			if position_object is None:
				position = Position({
					'position': position,
					'song_id': song_object.id,
					'chart_date': date,
					'chart_type': chart_type,
				})
				position = position.save()


if __name__ == '__main__':
	date_to_start = datetime(2024, 3, 1)
	while date_to_start < datetime.now():
		fill_db_chart(date_to_start)
		date_to_start += timedelta(days=7)
