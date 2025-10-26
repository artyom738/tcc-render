from model.entity.chart import Chart
from model.repository.chart_repository import chart_repository
from model.repository.position_repository import position_repository
from model.repository.song_repository import song_repository

months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


def get_tcc_title(chart: Chart):
	date = chart.chart_date
	#  Top Club Chart #468 (1 июня 2024) - ТОП 25 Танцевальных Треков
	return f'Top Club Chart #{chart.chart_number} ({date.strftime("%d")} {months[date.month - 1]} {date.strftime("%Y")}) - ТОП 25 Танцевальных треков'


def get_tcc_description(chart: Chart):
	result = f'''Top Club Chart - твой гид в мире актуальной танцевальной музыки!
Топ 25 главных клубных треков недели вместе с Тимуром Бодровым формируют лучшие диджеи России.
Они делают правильный выбор и делятся профессиональным мнением.
Присоединяйся к самому большому радиотанцполу страны!

Топ Клаб Чарт выходит на радиостанции "Европа Плюс" каждую субботу в 20:00 (мск)

ТРЕКЛИСТ:\n'''
	positions = position_repository.get_chart_positions(chart.id)
	for position in positions:
		song = song_repository.get_song_by_id(position.song_id)
		result += (str(position.position) + '. ' + song.authors + ' - ' + song.name + '\n')

	result += f'\nПосмотреть чарт - https://europaplus.ru/programs/top-club-chart?date={chart.chart_date.strftime("%Y-%m-%d")}\n'
	result += '#topclubchart #europaplus\n'
	return result


def get_eht_title(chart: Chart):
	date = chart.chart_date
	#  Еврохит Топ 40 (31 мая 2024) - 40 Главных Хитов Недели
	return f'Еврохит Топ 40 ({date.strftime("%d")} {months[date.month - 1]} {date.strftime("%Y")}) - 40 Главных Хитов Недели'


def get_eht_description(chart: Chart):
	result = f'''Еврохит Топ 40 - главный музыкальный чарт Европы Плюс!
Лучшие 40 песен недели, а также обзор западных чартов и интервью с артистами. 
Слушай каждую пятницу с 14:00 до 16:00 и каждую субботу с 16:00 до 18:00.

ТРЕКЛИСТ:\n'''
	positions = position_repository.get_chart_positions(chart.id)
	for position in positions:
		song = song_repository.get_song_by_id(position.song_id)
		result += (str(position.position) + '. ' + song.authors + ' - ' + song.name + '\n')

	result += f'\nПосмотреть чарт - https://europaplus.ru/programs/top40?date={chart.chart_date.strftime("%Y-%m-%d")}\n'
	result += '#eurohittop40 #europaplus\n'
	return result


def get_dark_title(chart: Chart):
	date = chart.chart_date
	#  Darknity Top 50 #10 (04.05.2024) - Чарт радио D1R
	return f'Darknity Top 50 #{chart.chart_number} ({date.strftime("%d.%m.%Y")}) - Чарт радио D1R'


def get_dark_description(chart: Chart):
	result = f'''Darknity Top 50 - актуальные хиты и новинки сезона от авторов Dark Sky Chart! Чарт создан на основе ротаций радио D1R.
Слушай каждую субботу с 18:00 до 20:00 (мск) на радио D1R!

Запускай радио D1R по прямой ссылке или добавляй в любимый плеер - https://listen7.myradio24.com/darknity

ТРЕКЛИСТ:\n'''
	positions = position_repository.get_chart_positions(chart.id)
	for position in positions:
		song = song_repository.get_song_by_id(position.song_id)
		result += str(position.position) + '. ' + song.authors + ' - ' + song.name + '\n'
	return result


def get_yt_title(chart: Chart):
	if chart.chart_type == 'tcc':
		return get_tcc_title(chart)
	if chart.chart_type == 'eht':
		return get_eht_title(chart)
	if chart.chart_type == 'dark':
		return get_dark_title(chart)


def get_yt_description(chart: Chart):
	if chart.chart_type == 'tcc':
		return get_tcc_description(chart)
	if chart.chart_type == 'eht':
		return get_eht_description(chart)
	if chart.chart_type == 'dark':
		return get_dark_description(chart)


def get_tags(chart: Chart):
	year = chart.chart_date.strftime("%Y")
	if chart.chart_type == 'tcc':
		return f'top club chart,танцевальная музыка {year},топ клаб чарт,хит парад европа плюс,топ клаб чарт {chart.chart_date.strftime("%d.%m")},top club chart europa plus,top club chart {year},европа плюс топ клаб чарт,top 25 chart,танцевальный чарт,клубный чарт {year},edm музыка {year},dance songs,чарт европа плюс,топ 25 европа плюс,европа плюс,чарт суббота европа плюс,ткч {chart.chart_number},tcc {chart.chart_number},топ клаб чарт последний выпуск,топ чарт европа плюс'
	if chart.chart_type == 'eht':
		return f'еврохит топ 40,топ чарт,хиты {year},европа плюс {year} топ 40 новинки,хит парад европа плюс,танцевальный чарт,танцевальная музыка {year},клубный чарт {year},новая музыка {year},dance songs,чарт европа плюс,европа плюс,итоговый чарт недели,чарт пятница европа плюс,евро хит топ 40,еврохит топ 40 последний выпуск,европа плюс {year},еврохит {chart.chart_date.strftime("%d.%m")},еврохит топ 40 {year},europe plus,хит топ 40'
	if chart.chart_type == 'dark':
		return f'dark sky chart,танцевальная музыка {year},новая музыка чарт,хит парад,darknity top 50,top 50 dance chart,radio d1r,d1r chart,радио диван,музыка в машину,музыка в машину {year} зарубежные,дип хаус музыка,прогрессив хаус музыка,хаус музыка подборка'


if __name__ == '__main__':
	chart_id = 92

	result = ''
	chart = chart_repository.get_chart_by_id(chart_id)
	if chart.chart_type == 'tcc':
		print(get_tcc_title(chart))
		print(get_tcc_description(chart))
		print(get_tags(chart))
	if chart.chart_type == 'eht':
		print(get_eht_title(chart))
		print(get_eht_description(chart))
		print(get_tags(chart))
	if chart.chart_type == 'dark':
		print(get_dark_title(chart))
		print(get_dark_description(chart))
		print(get_tags(chart))
