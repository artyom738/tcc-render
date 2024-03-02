import database


class Rubric:
	def __init__(self, data):
		self.rubric_type = data.get('rubric_type')
		self.song_id = data.get('song_id')
		self.chart_id = data.get('chart_id')

	def save(self):
		query = "insert into chart_rubrics (CHART_ID, SONG_ID, RUBRIC_TYPE) values (%s, %s, %s)"
		result = database.add(query, (
			self.chart_id or '',
			self.song_id or '',
			self.rubric_type or 0
		))

		return self
