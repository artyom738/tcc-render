from datetime import datetime

from model.repository.position_repository import PositionRepository
from model.repository.song_repository import SongRepository


def print_tcc_description(chart_date: datetime):
	print(f'''Top Club Chart - твой гид в мире актуальной танцевальной музыки!
Топ 25 главных клубных треков недели вместе с Тимуром Бодровым формируют лучшие диджеи России.
Они делают правильный выбор и делятся профессиональным мнением.
Присоединяйся к самому большому радиотанцполу страны!

Топ Клаб Чарт выходит на радиостанции "Европа Плюс" каждую субботу в 20:00 (мск)

ТРЕКЛИСТ:''')
	position_repo = PositionRepository('tcc')
	song_repo = SongRepository()
	positions = position_repo.get_positions_by_date(chart_date)
	for position in positions:
		song = song_repo.get_song_by_id(position.song_id)
		print(str(position.position) + '. ' + song.authors + ' - ' + song.name)

	print(f'\nПосмотреть чарт - https://europaplus.ru/top-club-chart?section=top25&date={chart_date.strftime("%Y-%m-%d")}\n')


def print_eht_description(chart_date: datetime):
	print(f'''Еврохит Топ 40 ({chart_date.strftime("%d.%m.%Y")}) - 40 Главных Хитов Недели
Еврохит Топ 40 - главный музыкальный чарт Европы Плюс!
Лучшие 40 песен недели, а также обзор западных чартов и интервью с артистами. 
Слушай каждую пятницу с 14:00 до 16:00 и каждую субботу с 16:00 до 18:00.

ТРЕКЛИСТ:''')
	position_repo = PositionRepository('eht')
	song_repo = SongRepository()
	positions = position_repo.get_positions_by_date(chart_date)
	for position in positions:
		song = song_repo.get_song_by_id(position.song_id)
		print(str(position.position) + '. ' + song.authors + ' - ' + song.name)

	print(f'\nПосмотреть чарт - https://europaplus.ru/top40?section=top40&date={chart_date.strftime("%Y-%m-%d")}\n')


def print_dark_description(chart_date: datetime):
	print(f'''Darknity Top 50 ({chart_date.strftime("%d.%m.%Y")}) - Чарт радио D1R
Darknity Top 50 - актуальные хиты и новинки сезона от авторов Dark Sky Chart! Создан на основе ротаций радио D1R.
Слушай каждую субботу с 18:00 до 20:00 (мск) на радио D1R!

Запускай радио D1R по прямой ссылке или добавляй в любимый плеер - https://listen7.myradio24.com/darknity

ТРЕКЛИСТ:''')
	position_repo = PositionRepository('dark')
	song_repo = SongRepository()
	positions = position_repo.get_positions_by_date(chart_date)
	for position in positions:
		song = song_repo.get_song_by_id(position.song_id)
		print(str(position.position) + '. ' + song.authors + ' - ' + song.name)



def __main__():
	chart_date = datetime(2024, 3, 15)
	# chart_type = 'eht'
	# chart_type = 'tcc'
	chart_type = 'dark'

	if chart_type == 'tcc':
		print_tcc_description(chart_date)
	if chart_type == 'eht':
		print_eht_description(chart_date)
	if chart_type == 'dark':
		print_dark_description(chart_date)


if __name__ == '__main__':
	__main__()
