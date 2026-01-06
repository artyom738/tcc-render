from datetime import datetime
import moviepy.editor as mp
from clips.position import text_font

from charts.eht_ny import EhtNy
from model.repository.chart_repository import chart_repository


class EhtNyPoints(EhtNy):
	def get_additional_stat_info(self, song: 'Song'):
		ny_chart = chart_repository.get_last_chart_by_type('eht_ny').fill()
		position_info = 'В итогах не был'
		for ny_chart_position in ny_chart.positions:
			if ny_chart_position.song_id == song.id:
				position_info = f'В итогах: #{ny_chart_position.position}'

		# Supposing we create chart after year chart release in next calendar year
		current_year = datetime.now().year
		year_for_chart = current_year - 1
		points_info = f'Очков в {year_for_chart}: {song.get_points("eht", datetime.strptime(f'{year_for_chart}-01-01', "%Y-%m-%d"), datetime.strptime(f'{current_year}-01-01', "%Y-%m-%d"))}'

		return position_info + '\n' + points_info

	def get_intro(self):
		intro_video = mp.VideoFileClip(
			'package/eht/intro-ny.mp4',
			target_resolution=(1080, 1920)
		)

		current_year = datetime.now().year
		year_for_chart = current_year - 1
		text_clip = (mp.TextClip(
			f'Сумма очков за {year_for_chart} год',
			fontsize=100,
			color='white',
			font=text_font,
			stroke_color='black',
			stroke_width=2
		).set_duration(intro_video.duration).set_position(['center', 860]))

		return mp.CompositeVideoClip([intro_video, text_clip])
