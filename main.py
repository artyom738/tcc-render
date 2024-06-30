from charts.factory import ChartFactory
from connectors.connector_factory import ConnectorFactory
from model.repository.chart_repository import chart_repository
from yt_clip_downloader import fill_songs_with_no_clip
from yt_uploader import YTUploader

if __name__ == '__main__':

	# chart_type = 'eht'
	chart_type = 'tcc'
	# chart_type = 'dark'

	rubrics = {
		############# ------------- EUROHIT TOP 40 ------------- #############
		'new_author': 'Kris Kross Amsterdam, INNA',  # Взгляд в будущее
		'new_name': 'Queen Of My Castle',
		'past_author': 'Nessa Barrett feat. jxdn',  # Сегодня завтра вчера
		'past_name': 'la di die',

		############# ------------- TOP CLUB CHART ------------- #############
		'residance_author': 'Goom Gum',  # 0:25:30 in podcast and 0:30:30 in radio
		'residance_name': 'Don\'t Wake Up',
		'alltime_author': 'Route 94 feat. Jess Glynne',  # 1:12:00 in podcast and 1:28:30 in radio
		'alltime_name': 'My Love',
		'perspective_author': 'Jamie xx, Robyn',  # 1:30:00 in podcast and 1:52:30 in radio
		'perspective_name': 'Life',
	}

	# chart_id = None
	chart_id = 109
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
