from datetime import datetime

from charts.eht_40 import Eht40
from charts.top_club_chart import TopClubChart
from model.entity.chart import Chart


def __main__(chart: Chart):
	TopClubChart(chart).render()
	# Eht40(chart).render()

if __name__ == '__main__':
	# Chart date format YYYY-MM-DD
	chart = Chart(data={
		'chart_number': 456,
		'chart_date': datetime(2024, 3, 9),
		'chart_type': 'tcc',
		# 'chart_type': 'eht',
	})
	__main__(chart)
