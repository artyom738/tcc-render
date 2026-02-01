from charts.factory import ChartFactory
from connectors.connector_factory import ConnectorFactory
from model.repository.chart_repository import chart_repository
from rubrics.finder_factory import RubricFinderFactory
from yt_clip_downloader import fill_songs_with_no_clip
# from yt_uploader import YTUploader

if __name__ == '__main__':

	# chart_type = 'eht'
	chart_type = 'tcc'
	# chart_type = 'dark'
	# chart_type = 'list'
	# chart_type = 'tcc_ny'

	rubrics = {
		############# ------------- EUROHIT TOP 40 ------------- #############
		'new_author': 'Harry Styles',  # Взгляд в будущее
		'new_name': 'Aperture',
		'past_author': 'Coldplay',  # Сегодня завтра вчера
		'past_name': 'Adventure Of A Lifetime',

		############# ------------- TOP CLUB CHART ------------- #############
		'residance_author': 'Aspyer & BRØMANCE',  # 0:25:30 in podcast and 0:30:30 in radio
		'residance_name': 'Higher',
		'perspective_author': 'KH, Four Tet, Nelly Furtado',  # 1:30:00 in podcast and 1:52:30 in radio
		'perspective_name': 'Only Human (MPH Remix)',
		'alltime_author': 'Eric Prydz ft. Rob Swire',  # 1:12:00 in podcast and 1:28:30 in radio
		'alltime_name': 'Breathe',
	}

	# chart_id = None
	chart_id = 176

	if chart_id:
		chart = chart_repository.get_chart_by_id(chart_id)
	else:
		connector = ConnectorFactory().get_connector(chart_type)
		chart = connector.create_next_chart()
		if chart_type == 'tcc' and not chart_id:
			# rubrics = RubricFinderFactory.get_rubric_finder(chart_type).find_rubrics(chart.chart_date)
			pass
		chart.save()
		connector.save_chart_data(chart)  # For darknity put json_data in DarkConnector first
		connector.save_rubrics(chart.id, rubrics)

	fill_songs_with_no_clip()  # Download clips - enable VPN first
	chart = chart.fill()
	renderable_chart = ChartFactory().create_chart(chart)
	if renderable_chart:
		renderable_chart.render()

	# YTUploader().upload_video(chart)
