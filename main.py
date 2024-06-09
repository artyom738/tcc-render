from charts.factory import ChartFactory
from connectors.connector_factory import ConnectorFactory
from model.repository.chart_repository import chart_repository
from yt_clip_downloader import fill_songs_with_no_clip
from yt_uploader import YTUploader

if __name__ == '__main__':

	chart_type = 'eht'
	# chart_type = 'tcc'
	# chart_type = 'dark'

	rubrics = {
		############# ------------- EUROHIT TOP 40 ------------- #############
		'new_author': 'Eminem',  # Взгляд в будущее
		'new_name': 'Houdini',
		'past_author': 'Calvin Harris, Disciples',  # Сегодня завтра вчера
		'past_name': 'How Deep Is Your Love',

		############# ------------- TOP CLUB CHART ------------- #############
		'residance_author': 'Swanky Tunes',  # 0:25:30 in podcast and 0:30:30 in radio
		'residance_name': 'Maneye',
		'alltime_author': 'Ministers De La Funk & Jocelyn Brown',  # 1:12:00 in podcast and 1:28:30 in radio
		'alltime_name': 'Believe',
		'perspective_author': 'Fred again.. & Anderson Paak',  # 1:30:00 in podcast and 1:52:30 in radio
		'perspective_name': 'places to be',
	}

	# chart_id = None
	chart_id = 99
	if chart_id:
		chart = chart_repository.get_chart_by_id(chart_id)
	else:
		connector = ConnectorFactory().get_connector(chart_type)
		chart = connector.create_next_chart()
		connector.save_chart_data(chart)  # For darknity put json_data in DarkConnector first
		connector.save_rubrics(chart.id, rubrics)

	fill_songs_with_no_clip()  # Download clips - enable VPN first
	chart = chart.fill()
	renderable_chart = ChartFactory().create_chart(chart)
	if renderable_chart:
		renderable_chart.render()

	# YTUploader().upload_video(chart)
