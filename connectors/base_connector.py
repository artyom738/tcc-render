from datetime import date, timedelta

from model.entity.chart import Chart
from model.repository.chart_repository import chart_repository


class BaseConnector:
	def save_positions(self, chart: Chart, data: list) -> None:
		raise NotImplementedError

	def create_next_chart(self) -> Chart:
		chart = Chart({
			'id': None,
			'chart_number': self.get_last_chart_number() + 1,
			'chart_date': self.get_last_chart_date(),
			'chart_type': self.get_chart_type(),
		}).save()

		return chart

	def get_last_chart_number(self) -> int:
		chart_type = self.get_chart_type()
		chart = chart_repository.get_last_chart_by_type(chart_type)
		if not chart:
			return 1
		return chart.chart_number

	def get_chart_type(self) -> str:
		raise NotImplementedError

	def get_last_chart_date(self) -> date:
		raise NotImplementedError

	def save_chart_data(self, chart: Chart) -> None:
		data = self.get_data(chart)
		self.save_positions(chart, data)

	def get_data(self, chart: Chart) -> list:
		raise NotImplementedError

	def save_rubrics(self, chart_id: int, rubrics: dict):
		raise NotImplementedError
