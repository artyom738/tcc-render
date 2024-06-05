from datetime import datetime

from charts.factory import ChartFactory
from model.repository.chart_repository import chart_repository

if __name__ == '__main__':
	chart = chart_repository.get_chart_by_id(94)
	chart.fill()
	renderable_chart = ChartFactory().create_chart(chart)
	if renderable_chart:
		renderable_chart.render()
