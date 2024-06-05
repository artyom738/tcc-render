from model.repository.chart_repository import chart_repository
from model.repository.position_repository import position_repository
from model.repository.song_repository import song_repository


def print_tcc_description(chart: 'Chart'):
	print(f'''Top Club Chart - твой гид в мире актуальной танцевальной музыки!
Топ 25 главных клубных треков недели вместе с Тимуром Бодровым формируют лучшие диджеи России.
Они делают правильный выбор и делятся профессиональным мнением.
Присоединяйся к самому большому радиотанцполу страны!

Топ Клаб Чарт выходит на радиостанции "Европа Плюс" каждую субботу в 20:00 (мск)

ТРЕКЛИСТ:''')
	positions = position_repository.get_chart_positions(chart.id)
	for position in positions:
		song = song_repository.get_song_by_id(position.song_id)
		print(str(position.position) + '. ' + song.authors + ' - ' + song.name)

	print(f'\nПосмотреть чарт - https://europaplus.ru/top-club-chart?section=top25&date={chart.chart_date.strftime("%Y-%m-%d")}\n')
	print('#topclubchart #europaplus\n')


def print_eht_description(chart: 'Chart'):
	print(f'''Еврохит Топ 40 ({chart.chart_date.strftime("%d.%m.%Y")}) - 40 Главных Хитов Недели
Еврохит Топ 40 - главный музыкальный чарт Европы Плюс!
Лучшие 40 песен недели, а также обзор западных чартов и интервью с артистами. 
Слушай каждую пятницу с 14:00 до 16:00 и каждую субботу с 16:00 до 18:00.

ТРЕКЛИСТ:''')
	positions = position_repository.get_chart_positions(chart.id)
	for position in positions:
		song = song_repository.get_song_by_id(position.song_id)
		print(str(position.position) + '. ' + song.authors + ' - ' + song.name)

	print(f'\nПосмотреть чарт - https://europaplus.ru/top40?section=top40&date={chart.chart_date.strftime("%Y-%m-%d")}\n')
	print('#eurohittop40 #europaplus\n')


def print_dark_description(chart: 'Chart'):
	print(f'''Darknity Top 50 #{chart.chart_number} ({chart.chart_date.strftime("%d.%m.%Y")}) - Чарт радио D1R
Darknity Top 50 - актуальные хиты и новинки сезона от авторов Dark Sky Chart! Чарт создан на основе ротаций радио D1R.
Слушай каждую субботу с 18:00 до 20:00 (мск) на радио D1R!

Запускай радио D1R по прямой ссылке или добавляй в любимый плеер - https://listen7.myradio24.com/darknity

ТРЕКЛИСТ:''')
	positions = position_repository.get_chart_positions(chart.id)
	for position in positions:
		song = song_repository.get_song_by_id(position.song_id)
		print(str(position.position) + '. ' + song.authors + ' - ' + song.name)


if __name__ == '__main__':
	chart_id = 94

	chart = chart_repository.get_chart_by_id(chart_id)
	if chart.chart_type == 'tcc':
		print_tcc_description(chart)
	if chart.chart_type == 'eht':
		print_eht_description(chart)
	if chart.chart_type == 'dark':
		print_dark_description(chart)
