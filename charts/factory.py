from __future__ import annotations

from charts.darknity import Darknity
from model.entity.chart import Chart
from charts.base_chart import BaseChart
from charts.top_club_chart import TopClubChart
from charts.eht_40 import Eht40


class ChartFactory:
	def create_chart(self, chart: Chart) -> BaseChart | None:
		if chart.chart_type == 'tcc':
			return TopClubChart(chart)
		elif chart.chart_type == 'eht':
			return Eht40(chart)
		elif chart.chart_type == 'dark':
			return Darknity(chart)
		else:
			print('Chart factory doesn`t know about chart')
			return None
