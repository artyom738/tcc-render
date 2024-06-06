import requests

from datetime import datetime

from model.entity.chart import Chart
from model.entity.position import Position
from model.entity.rubric import Rubric
from model.entity.song import Song
from model.repository.chart_rubrics_repository import chart_rubric_repository
from model.repository.position_repository import position_repository
from model.repository.song_repository import song_repository


def fill_db_chart(chart: Chart):
	str_date = chart.chart_date.strftime("%Y-%m-%d")
	api_url = "https://europaplus.ru/api/programs/top-club-chart?date=" + str_date
	response = requests.get(api_url)
	res = response.json()

	data = res['data']
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
				})
				song_object = song_object.save()
			position_object = position_repository.get_position_in_chart(song_object.id, chart.id)
			if position_object is None:
				position = Position({
					'position': position,
					'song_id': song_object.id,
					'chart_id': chart.id,
				})
				position = position.save()


def fill_rubrics(chart_id: int, rubric_songs: dict):
	if not chart_id:
		return

	if rubric_songs['alltime_name'] and rubric_songs['alltime_author']:
		alltime_song = Song({
			'name': rubric_songs['alltime_name'],
			'authors': rubric_songs['alltime_author'],
			'ep_id': None,
		}).save()
		Rubric({
			'chart_id': chart_id,
			'song_id': alltime_song.id,
			'rubric_type': chart_rubric_repository.RUBRIC_ALL_TIME,
			'chart_type': 'tcc',
		}).save()

	if rubric_songs['residance_name'] and rubric_songs['residance_author']:
		alltime_song = Song({
			'name': rubric_songs['residance_name'],
			'authors': rubric_songs['residance_author'],
			'ep_id': None,
		}).save()
		Rubric({
			'chart_id': chart_id,
			'song_id': alltime_song.id,
			'rubric_type': chart_rubric_repository.RUBRIC_RESIDANCE,
			'chart_type': 'tcc',
		}).save()

	if rubric_songs['perspective_name'] and rubric_songs['perspective_author']:
		alltime_song = Song({
			'name': rubric_songs['perspective_name'],
			'authors': rubric_songs['perspective_author'],
			'ep_id': None,
		}).save()
		Rubric({
			'chart_id': chart_id,
			'song_id': alltime_song.id,
			'rubric_type': chart_rubric_repository.RUBRIC_PERSPECTIVE,
			'chart_type': 'tcc',
		}).save()


if __name__ == '__main__':
	chart = Chart({
		'id': None,
		'chart_number': 468,
		'chart_date': '2024-06-01',
		'chart_type': 'tcc',
	}).save()
	fill_db_chart(chart)
	need_fill_rubrics = True
	if need_fill_rubrics:
		fill_rubrics(chart.id, {
			'residance_author': 'Going Deeper, ARIA',  # 0:25:30 in podcast and 0:30:30 in radio
			'residance_name': 'Out Of Control',
			'alltime_author': 'York',  # 1:12:00 in podcast and 1:28:30 in radio
			'alltime_name': 'On The Beach',
			'perspective_author': 'Skrillex, Hamdi, Taichu',  # 1:30:00 in podcast and 1:52:30 in radio
			'perspective_name': 'Push',
		})

