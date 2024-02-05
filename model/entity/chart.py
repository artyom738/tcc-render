from datetime import datetime
from model.repository.position_repository import PositionRepository

from model.repository.song_repository import SongRepository


class Chart:
	def __init__(self, data):
		self.chart_number: int = data.get('chart_number')
		self.chart_date: datetime = data.get('chart_date')
		self.positions: list = []
		self.outs: list = []
		self.fill()

	def fill(self):
		repo = PositionRepository()
		self.positions = repo.get_positions_by_date(self.chart_date)
		self.outs = repo.get_outs_by_date(self.chart_date)
		self.fill_max_up_down()
		self.fill_lcs()

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
			weeks = song.get_weeks()
			if weeks >= max_weeks:
				max_weeks = weeks
				lcs_positions.append(position.position)

		for position in self.positions:
			if position.position in lcs_positions:
				position.is_lcs = True

	def get_lcs(self):
		for position in self.positions:
			if position.is_lcs:
				return position
