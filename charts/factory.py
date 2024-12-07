from charts.darknity import Darknity
from model.entity.chart import Chart
from charts.base_chart import BaseChart
from charts.top_club_chart import TopClubChart
from charts.eht_40 import Eht40
from charts.list import List


class ChartFactory:
	def create_chart(self, chart: Chart) -> BaseChart:
		if chart.chart_type == 'tcc':
			return TopClubChart(chart)
		elif chart.chart_type == 'eht':
			return Eht40(chart)
		elif chart.chart_type == 'dark':
			return Darknity(chart)
		elif chart.chart_type == 'list':
			return List(chart)
		else:
			raise ValueError('Chart factory doesn`t know about this type of chart')
