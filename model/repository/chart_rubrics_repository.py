import database
from model.entity.rubric import Rubric


class ChartRubricsRepository:
	RUBRIC_ALL_TIME = 'A'
	RUBRIC_RESIDANCE = 'R'
	RUBRIC_PERSPECTIVE = 'P'

	def __init__(self, chart_type: str):
		self.chart_type: str = chart_type

	def get_rubrics_by_chart_id(self, chart_id: int) -> list[Rubric]:
		query = f'select * from chart_rubrics where CHART_ID = {str(chart_id)} and CHART_TYPE = \'{self.chart_type}\''
		db_result = database.get_list(query)
		result = []
		if len(db_result) > 0:
			for position in db_result:
				result.append(self.fetch_object(position))
			return result
		else:
			return []

	def fetch_object(self, data: dict) -> Rubric:
		return Rubric({
			'chart_id': data['CHART_ID'],
			'song_id': data['SONG_ID'],
			'rubric_type': data['RUBRIC_TYPE'],
			'chart_type': data['CHART_TYPE'],
		})
