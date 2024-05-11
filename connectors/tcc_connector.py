import json.encoder

import requests

from datetime import datetime, timedelta
from model.entity.position import Position
from model.entity.rubric import Rubric
from model.entity.song import Song
from model.repository.chart_rubrics_repository import ChartRubricsRepository
from model.repository.position_repository import PositionRepository
from model.repository.song_repository import SongRepository


def fill_db_chart(date: datetime):
	str_date = date_to_start.strftime("%Y-%m-%d")
	api_url = "https://europaplus.ru/api/programs/top-club-chart?date=" + str_date
	response = requests.get(api_url)
	res = response.json()
	chart_type = 'tcc'

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
					'ep_id': ep_id or 0,
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


def fill_rubrics(chart_number: int, rubric_songs: dict):
	if not chart_number:
		return

	if rubric_songs['alltime_name'] and rubric_songs['alltime_author']:
		alltime_song = Song({
			'name': rubric_songs['alltime_name'],
			'authors': rubric_songs['alltime_author'],
			'ep_id': None,
		}).save()
		Rubric({
			'chart_id': chart_number,
			'song_id': alltime_song.id,
			'rubric_type': ChartRubricsRepository.RUBRIC_ALL_TIME,
			'chart_type': 'tcc',
		}).save()

	if rubric_songs['residance_name'] and rubric_songs['residance_author']:
		alltime_song = Song({
			'name': rubric_songs['residance_name'],
			'authors': rubric_songs['residance_author'],
			'ep_id': None,
		}).save()
		Rubric({
			'chart_id': chart_number,
			'song_id': alltime_song.id,
			'rubric_type': ChartRubricsRepository.RUBRIC_RESIDANCE,
			'chart_type': 'tcc',
		}).save()

	if rubric_songs['perspective_name'] and rubric_songs['perspective_author']:
		alltime_song = Song({
			'name': rubric_songs['perspective_name'],
			'authors': rubric_songs['perspective_author'],
			'ep_id': None,
		}).save()
		Rubric({
			'chart_id': chart_number,
			'song_id': alltime_song.id,
			'rubric_type': ChartRubricsRepository.RUBRIC_PERSPECTIVE,
			'chart_type': 'tcc',
		}).save()


if __name__ == '__main__':
	date_to_start = datetime(2024, 5, 11)
	while date_to_start < datetime.now():
		fill_db_chart(date_to_start)
		date_to_start += timedelta(days=7)
		need_fill_rubrics = True
		if need_fill_rubrics:
			chart_number = 465
			fill_rubrics(chart_number, {
				'residance_author': 'Vion Konger & Blasterjaxx',  # 0:25:30 in podcast and 0:30:30 in radio
				'residance_name': 'Feel The Bass',
				'alltime_author': 'Modo',  # 1:12:00 in podcast and 1:28:30 in radio
				'alltime_name': 'Ein Zwei Polizei',
				'perspective_author': 'Majestic, The Jammin Kid, Celine Dion',  # 1:30:00 in podcast and 1:52:30 in radio
				'perspective_name': 'Set My Heart On Fire',
			})
