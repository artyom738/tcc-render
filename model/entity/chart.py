from __future__ import annotations
from datetime import datetime

import database
from model.repository.chart_rubrics_repository import chart_rubric_repository
from model.repository.song_repository import song_repository


class Chart:
	def __init__(self, data):
		self.id: int = data.get('id')
		self.chart_number: int = data.get('chart_number')
		self.chart_date: datetime = data.get('chart_date')
		self.chart_type: str = data.get('chart_type')
		self.positions: list = []
		self.outs: list = []
		self.rubric: dict = {}
		self.all_time_song_id: int | None = None
		self.residance_song_id: int | None = None
		self.perspective_song_id: int | None = None

	def fill(self):
		from model.repository.position_repository import position_repository
		self.positions = position_repository.get_chart_positions(self.id)
		self.outs = position_repository.get_chart_outs(self.id)
		self.fill_max_up_down()
		self.fill_lcs()
		self.fill_rubrics()
		return self

	def fill_max_up_down(self):
		max_up = 0
		max_down = 0
		for position in self.positions:
			lw = position.get_lw()
			if lw == '--' or lw is None:
				continue
			if lw - position.position > max_up:
				max_up = lw - position.position
			if lw - position.position < max_down:
				max_down = lw - position.position

		for position in self.positions:
			lw = position.get_lw()
			if lw == '--' or lw is None:
				continue
			if lw - position.position > 0 and lw - position.position == max_up:
				position.moving = 'double-up'
			if lw - position.position < 0 and lw - position.position == max_down:
				position.moving = 'double-down'

	# Longest Chart Sitter
	def fill_lcs(self):
		max_weeks = 0
		lcs_positions = []
		for position in self.positions:
			song = song_repository.get_song_by_id(position.song_id)
			weeks = song.get_weeks(self.chart_type)
			if weeks >= max_weeks:
				max_weeks = weeks

		for position in self.positions:
			song = song_repository.get_song_by_id(position.song_id)
			weeks = song.get_weeks(self.chart_type)
			if weeks == max_weeks:
				lcs_positions.append(position.position)

		for position in self.positions:
			if position.position in lcs_positions:
				position.is_lcs = True

	def get_lcs(self):
		for position in self.positions:
			if position.is_lcs:
				return position

	def fill_rubrics(self):
		rubrics = chart_rubric_repository.get_rubrics_by_chart_id(self.id)
		for rubric in rubrics:
			if rubric.rubric_type == chart_rubric_repository.RUBRIC_ALL_TIME:
				self.rubric['all_time_song_id'] = rubric.song_id
			elif rubric.rubric_type == chart_rubric_repository.RUBRIC_RESIDANCE:
				self.rubric['residance_song_id'] = rubric.song_id
			elif rubric.rubric_type == chart_rubric_repository.RUBRIC_PERSPECTIVE:
				self.rubric['perspective_song_id'] = rubric.song_id
			elif rubric.rubric_type == chart_rubric_repository.RUBRIC_EHT_PERSPECTIVE:
				self.rubric['eht_perspective_song_id'] = rubric.song_id
			elif rubric.rubric_type == chart_rubric_repository.RUBRIC_EHT_OLD:
				self.rubric['eht_old_song_id'] = rubric.song_id

	def save(self):
		if self.id:
			query = "update charts set CHART_TYPE = %s, CHART_NUMBER = %s, CHART_DATE = %s WHERE ID = %s"
			result = database.add(query, (
				self.chart_type or '',
				self.chart_number or 0,
				self.chart_date or '',
				self.id
			))
		else:
			query = "insert into charts (CHART_TYPE, CHART_NUMBER, CHART_DATE) values (%s, %s, %s)"
			result = database.add(query, (
				self.chart_type or '',
				self.chart_number or 0,
				self.chart_date or ''
			))
			self.id = result

		return self
