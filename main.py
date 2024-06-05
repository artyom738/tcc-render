from datetime import datetime

from charts.factory import ChartFactory
from model.entity.chart import Chart


if __name__ == '__main__':
	# Chart date format YYYY-MM-DD
	# Current charts: tcc = 468, eht = 14, dark = 12
	chart = Chart(data={
		'chart_number': 12,
		'chart_date': datetime(2024, 5, 18),
		# 'chart_type': 'tcc',
		# 'chart_type': 'eht',
		'chart_type': 'dark',
	})
	renderable_chart = ChartFactory().create_chart(chart)
	if renderable_chart:
		renderable_chart.render()
