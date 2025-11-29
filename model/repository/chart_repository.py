from __future__ import annotations
from db import database
from model.entity.chart import Chart


class ChartRepository:
	def __init__(self):
		self.previous_charts = {}
		self.instance: ChartRepository | None = None

	def get_chart_by_id(self, chart_id: int) -> Chart | None:
		query = f'select * from charts where ID = {chart_id}'
		result = database.get_list(query)
		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def get_previous_chart(self, chart_id: int) -> Chart | None:
		if self.previous_charts.get(chart_id):
			return self.previous_charts.get(chart_id)

		current_chart = self.get_chart_by_id(chart_id)
		chart_type = current_chart.chart_type
		query = f'select * from charts where CHART_TYPE = \'{chart_type}\' and CHART_DATE <= \'{current_chart.chart_date}\' order by CHART_DATE desc'
		result = database.get_list(query)
		if len(result) > 1:
			self.previous_charts[chart_id] = self.fetch_object(result[1])
			return self.previous_charts.get(chart_id)
		else:
			return None

	def get_last_chart_by_type(self, chart_type: str):
		query = f'select * from charts where CHART_TYPE = \'{chart_type}\' order by CHART_DATE desc'
		result = database.get_list(query)
		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def get_last_chart(self) -> Chart | None:
		query = f'select * from charts order by ID desc'
		result = database.get_list(query)
		if len(result) > 0:
			return self.fetch_object(result[0])
		else:
			return None

	def fetch_object(self, data: dict) -> Chart:
		return Chart({
			'id': data['ID'],
			'chart_type': data['CHART_TYPE'],
			'chart_number': data['CHART_NUMBER'],
			'chart_date': data['CHART_DATE'],
		})


chart_repository = ChartRepository()
