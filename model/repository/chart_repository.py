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

	def get_next_chart_number(self, chart_type: str) -> int:
		query = 'select coalesce(max(CHART_NUMBER), 0) + 1 as next_number from charts where CHART_TYPE = %s'
		result = database.get_list(query, (chart_type,))
		if result and result[0].get('next_number') is not None:
			return int(result[0]['next_number'])
		return 1

	def get_full_chart(self, chart_id: int) -> dict | None:
		chart = self.get_chart_by_id(chart_id)
		if not chart:
			return None

		positions_query = (
			'select cp.POSITION, cp.SONG_ID, s.NAME, s.AUTHORS '
			'from chart_positions cp '
			'left join songs s on s.ID = cp.SONG_ID '
			'where cp.CHART_ID = %s and cp.POSITION > 0 and cp.POSITION < 300 '
			'order by cp.POSITION'
		)
		positions = database.get_list(positions_query, (chart_id,))

		rubrics_query = (
			'select r.RUBRIC_TYPE, r.SONG_ID, s.NAME, s.AUTHORS '
			'from chart_rubrics r '
			'left join songs s on s.ID = r.SONG_ID '
			'where r.CHART_ID = %s'
		)
		rubrics = database.get_list(rubrics_query, (chart_id,))

		return {
			'chart': chart,
			'positions': positions,
			'rubrics': rubrics,
		}

	def fetch_object(self, data: dict) -> Chart:
		return Chart({
			'id': data['ID'],
			'chart_type': data['CHART_TYPE'],
			'chart_number': data['CHART_NUMBER'],
			'chart_date': data['CHART_DATE'],
		})


chart_repository = ChartRepository()
