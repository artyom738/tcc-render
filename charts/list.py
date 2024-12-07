import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from moviepy.Clip import Clip
from datetime import datetime, date

from charts.base_chart import BaseChart
from clips.position import chart_number_font, text_font


class List(BaseChart):
	def get_chart_type(self) -> str:
		return 'list'

	def get_position_font_family(self) -> str:
		return 'Andes-Cnd-W04-SemiBold'

	def need_show_lcs(self):
		return False

	def need_save_preview(self) -> bool:
		return True

	def get_additional_stat_info(self, song: 'Song'):
		charts = song.get_charts(self.get_chart_type())

		if len(charts) == 0:
			return 'Не был в чарте'

		first = charts[0]
		last = charts[len(charts) - 1]

		if last['CHART_DATE'].strftime('%Y-%m-%d') == '2024-11-29':
			date_range = first['CHART_DATE'].strftime('%d.%m.%Y') + ' - наст. вр.'
		else:
			date_range = first['CHART_DATE'].strftime('%d.%m.%Y') + ' - ' + last['CHART_DATE'].strftime('%d.%m.%Y')

		if first['CHART_DATE'] < datetime.strptime('2024-01-01', '%Y-%m-%d').date():
			weeks_in_2024 = 0
			for chart in charts:
				if chart['CHART_DATE'] > datetime.strptime('2024-01-01', '%Y-%m-%d').date():
					weeks_in_2024 += 1
			return 'Недель в 2024 - ' + str(weeks_in_2024) + "\n" + date_range

		return date_range

	def get_intro(self):
		#  May be changed due to variable charts
		return mp.VideoFileClip(
			'package/eht/intro.mp4',
			target_resolution=(1080, 1920)
		)

	def generate_clip(self):
		songs_clip = self.get_positions(0, self.chart)
