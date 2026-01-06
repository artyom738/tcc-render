from datetime import datetime

from charts.list import List
from model.repository.chart_repository import chart_repository


class EhtPretenders(List):
	def need_show_lw_moving(self):
		return False

	def get_chart_type_for_stats(self):
		return 'eht'

	def get_additional_stat_info(self, song: 'Song'):
		charts = song.get_charts('eht')
		if len(charts) == 0:
			return 'Не был в чарте'

		first = charts[0]
		last = charts[len(charts) - 1]

		last_chart = chart_repository.get_last_chart_by_type('eht').fill()
		current_year = datetime.now().year

		if last['CHART_DATE'].strftime('%Y-%m-%d') == last_chart.chart_date.strftime('%Y-%m-%d'):
			date_range = first['CHART_DATE'].strftime('%d.%m.%Y') + ' - наст. вр.'
		else:
			date_range = first['CHART_DATE'].strftime('%d.%m.%Y') + ' - ' + last['CHART_DATE'].strftime('%d.%m.%Y')

		if first['CHART_DATE'] < datetime.strptime(f'{current_year}-01-01', '%Y-%m-%d').date():
			weeks_in_2025 = 0
			for chart in charts:
				if chart['CHART_DATE'] > datetime.strptime(f'{current_year}-01-01', '%Y-%m-%d').date():
					weeks_in_2025 += 1
			return f'Недель в {current_year} - ' + str(weeks_in_2025) + "\n" + date_range

		return date_range
