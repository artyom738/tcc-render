from datetime import datetime

from model.repository.position_repository import PositionRepository
from model.repository.song_repository import SongRepository


def __main__():
	chart_date = datetime(2024, 2, 24)
	position_repo = PositionRepository()
	song_repo = SongRepository()
	positions = position_repo.get_positions_by_date(chart_date)
	for position in positions:
		song = song_repo.get_song_by_id(position.song_id)
		print(str(position.position) + '. ' + song.authors + ' - ' + song.name)


if __name__ == '__main__':
	__main__()
