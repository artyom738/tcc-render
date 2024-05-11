from datetime import datetime

from charts.factory import ChartFactory
from model.entity.chart import Chart


def __main__(chart: Chart):
	renderable_chart = ChartFactory().create_chart(chart)
	if renderable_chart:
		renderable_chart.render()


if __name__ == '__main__':
	# Chart date format YYYY-MM-DD
	# Current charts: tcc = 465, eht = 11, dark = 9
	chart = Chart(data={
		'chart_number': 465,
		'chart_date': datetime(2024, 5, 11),
		'chart_type': 'tcc',
		# 'chart_type': 'eht',
		# 'chart_type': 'dark',
	})
	__main__(chart)
