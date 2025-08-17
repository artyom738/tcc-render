from datetime import datetime, timedelta, date

from connectors.europa_plus_connector import EuropaPlusConnector
from model.entity.chart import Chart
from model.entity.rubric import Rubric
from model.entity.song import Song
from model.repository.chart_rubrics_repository import chart_rubric_repository


class EurohitConnector(EuropaPlusConnector):
	def get_api_url(self, chart: Chart):
		str_date = chart.chart_date.strftime("%Y-%m-%d")
		return "https://europaplus.ru/api/programs/top40?date=" + str_date

	def get_chart_type(self) -> str:
		return 'eht'

	def get_last_chart_date(self) -> date:
		today = datetime.today()
		weekday = today.weekday()
		days_to_last_friday = (weekday - 4) % 7  # 4 matches friday
		last_friday = today - timedelta(days=days_to_last_friday)
		return last_friday.date()

	def save_rubrics(self, chart_id: int, rubrics: dict):
		if not chart_id:
			return

		if rubrics['new_name'] and rubrics['new_author']:
			rubric_song = Song({
				'name': rubrics['new_name'],
				'authors': rubrics['new_author'],
				'ep_id': None,
			}).save()
			Rubric({
				'chart_id': chart_id,
				'song_id': rubric_song.id,
				'rubric_type': chart_rubric_repository.RUBRIC_EHT_PERSPECTIVE,
				'chart_type': self.get_chart_type(),
			}).save()

		if rubrics['past_name'] and rubrics['past_author']:
			rubric_song = Song({
				'name': rubrics['past_name'],
				'authors': rubrics['past_author'],
				'ep_id': None,
			}).save()
			Rubric({
				'chart_id': chart_id,
				'song_id': rubric_song.id,
				'rubric_type': chart_rubric_repository.RUBRIC_EHT_OLD,
				'chart_type': self.get_chart_type(),
			}).save()


if __name__ == '__main__':
	date = '2025-01-10'
	chart_number = 9
	date_object = datetime.strptime(date, '%Y-%m-%d').date()
	while date_object < datetime.strptime('2025-08-16', '%Y-%m-%d').date():
		connector = EurohitConnector()
		chart = Chart({
			'id': None,
			'chart_number': chart_number,
			'chart_date': date_object,
			'chart_type': 'eht',
		}).save()
		connector.save_chart_data(chart)
		date_object += timedelta(days=7)
		chart_number += 1

	# need_fill_rubrics = False
	# if need_fill_rubrics:
	# 	connector.save_rubrics(chart.id, {
	# 		'new_author': 'Lost Frequencies feat. David Kushner',  # Взгляд в будущее
	# 		'new_name': 'In My Bones',
	# 		'past_author': 'Hurts',  # Сегодня завтра вчера
	# 		'past_name': 'Stay',
	# 	})
