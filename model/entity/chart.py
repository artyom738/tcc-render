from __future__ import annotations
from datetime import datetime

from model.repository.chart_rubrics_repository import ChartRubricsRepository
from model.repository.position_repository import PositionRepository
from model.repository.song_repository import SongRepository


class Chart:
	def __init__(self, data):
		self.chart_number: int = data.get('chart_number')
		self.chart_date: datetime = data.get('chart_date')
		self.chart_type: str = data.get('chart_type')
		self.positions: list = []
		self.outs: list = []
		self.rubric: dict = {}
		self.all_time_song_id: int | None = None
		self.residance_song_id: int | None = None
		self.perspective_song_id: int | None = None
		self.fill()

	def fill(self):
		repo = PositionRepository(self.chart_type)
		self.positions = repo.get_positions_by_date(self.chart_date)
		self.outs = repo.get_outs_by_date(self.chart_date)
		self.fill_max_up_down()
		self.fill_lcs()
		self.fill_rubrics()

	def fill_max_up_down(self):
		max_up = 0
		max_down = 0
		for position in self.positions:
			lw = position.get_lw()
			if lw == '--':
				continue
			if lw - position.position > max_up:
				max_up = lw - position.position
			if lw - position.position < max_down:
				max_down = lw - position.position

		for position in self.positions:
			lw = position.get_lw()
			if lw == '--':
				continue
			if lw - position.position > 0 and lw - position.position == max_up:
				position.moving = 'double-up'
			if lw - position.position < 0 and lw - position.position == max_down:
				position.moving = 'double-down'

	# Longest Chart Sitter
	def fill_lcs(self):
		max_weeks = 0
		song_repo = SongRepository()
		lcs_positions = []
		for position in self.positions:
			song = song_repo.get_song_by_id(position.song_id)
			weeks = song.get_weeks(self.chart_type)
			if weeks >= max_weeks:
				max_weeks = weeks

		for position in self.positions:
			song = song_repo.get_song_by_id(position.song_id)
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
		rubrics = ChartRubricsRepository(self.chart_type).get_rubrics_by_chart_id(self.chart_number)
		for rubric in rubrics:
			if rubric.rubric_type == ChartRubricsRepository.RUBRIC_ALL_TIME:
				self.rubric['all_time_song_id'] = rubric.song_id
			elif rubric.rubric_type == ChartRubricsRepository.RUBRIC_RESIDANCE:
				self.rubric['residance_song_id'] = rubric.song_id
			elif rubric.rubric_type == ChartRubricsRepository.RUBRIC_PERSPECTIVE:
				self.rubric['perspective_song_id'] = rubric.song_id
			elif rubric.rubric_type == ChartRubricsRepository.RUBRIC_EHT_PERSPECTIVE:
				self.rubric['eht_perspective_song_id'] = rubric.song_id
			elif rubric.rubric_type == ChartRubricsRepository.RUBRIC_EHT_OLD:
				self.rubric['eht_old_song_id'] = rubric.song_id
