import time
from datetime import datetime, timedelta, date

from connectors.europa_plus_connector import EuropaPlusConnector
from model.entity.chart import Chart
from model.entity.rubric import Rubric
from model.entity.song import Song
from model.repository.chart_rubrics_repository import chart_rubric_repository


class TopClubChartConnector(EuropaPlusConnector):

	def get_api_url(self, chart: Chart):
		str_date = chart.chart_date.strftime("%Y-%m-%d")
		return "https://europaplus.ru/api/programs/top-club-chart?date=" + str_date

	def get_chart_type(self) -> str:
		return 'tcc'

	def get_last_chart_date(self) -> date:
		today = datetime.today()
		weekday = today.weekday()
		days_to_last_saturday = (weekday - 5) % 7  # 5 matches saturday
		last_saturday = today - timedelta(days=days_to_last_saturday)
		return last_saturday.date()

	def save_rubrics(self, chart_id: int, rubrics: dict):
		if not chart_id:
			return

		if rubrics['alltime_name'] and rubrics['alltime_author']:
			rubric_song = Song({
				'name': rubrics['alltime_name'],
				'authors': rubrics['alltime_author'],
				'ep_id': None,
			}).save()
			Rubric({
				'chart_id': chart_id,
				'song_id': rubric_song.id,
				'rubric_type': chart_rubric_repository.RUBRIC_ALL_TIME,
				'chart_type': self.get_chart_type(),
			}).save()

		if rubrics['residance_name'] and rubrics['residance_author']:
			rubric_song = Song({
				'name': rubrics['residance_name'],
				'authors': rubrics['residance_author'],
				'ep_id': None,
			}).save()
			Rubric({
				'chart_id': chart_id,
				'song_id': rubric_song.id,
				'rubric_type': chart_rubric_repository.RUBRIC_RESIDANCE,
				'chart_type': self.get_chart_type(),
			}).save()

		if rubrics['perspective_name'] and rubrics['perspective_author']:
			rubric_song = Song({
				'name': rubrics['perspective_name'],
				'authors': rubrics['perspective_author'],
				'ep_id': None,
			}).save()
			Rubric({
				'chart_id': chart_id,
				'song_id': rubric_song.id,
				'rubric_type': chart_rubric_repository.RUBRIC_PERSPECTIVE,
				'chart_type': self.get_chart_type(),
			}).save()


if __name__ == '__main__':
	date = '2025-02-22'
	chart_number = 505
	date_object = datetime.strptime(date, '%Y-%m-%d').date()
	while date_object < datetime.strptime('2025-08-16', '%Y-%m-%d').date():
		connector = TopClubChartConnector()
		chart = Chart({
			'id': None,
			'chart_number': chart_number,
			'chart_date': date_object,
			'chart_type': 'tcc',
		}).save()
		connector.save_chart_data(chart)
		date_object += timedelta(days=7)
		print('Saved ' + str(chart_number))
		chart_number += 1
		time.sleep(2)


	# chart = Chart({
	# 	'id': None,
	# 	'chart_number': 468,
	# 	'chart_date': '2024-06-01',
	# 	'chart_type': 'tcc',
	# }).save()
	# connector = TopClubChartConnector()
	# connector.save_chart_data(chart)
	# need_fill_rubrics = True
	# if need_fill_rubrics:
	# 	connector.save_rubrics(chart.id, {
	# 		'residance_author': 'Going Deeper, ARIA',  # 0:25:30 in podcast and 0:30:30 in radio
	# 		'residance_name': 'Out Of Control',
	# 		'alltime_author': 'York',  # 1:12:00 in podcast and 1:28:30 in radio
	# 		'alltime_name': 'On The Beach',
	# 		'perspective_author': 'Skrillex, Hamdi, Taichu',  # 1:30:00 in podcast and 1:52:30 in radio
	# 		'perspective_name': 'Push',
	# 	})
