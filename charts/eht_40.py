import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from moviepy.Clip import Clip

from charts.base_chart import BaseChart
from clips.position import chart_number_font, text_font


class Eht40(BaseChart):
	def get_chart_type(self) -> str:
		return 'eht'

	def get_position_text_color(self, position: int = 0):
		if position <= 5:
			return '#ed9b2b'  # Orange
		return '#1566af'  # Blue

	def get_last_out_composition(self) -> list[Clip]:
		clip_chart_number = mp.TextClip(
			txt='Еврохит Топ 40', font=chart_number_font,
			color='#36c2f8', fontsize=180, stroke_color='white',
			stroke_width=5, align='center',
		) \
			.set_duration(3) \
			.set_position(('center', 400)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		clip_chart_date = mp.TextClip(
			txt=str(self.chart.chart_date.strftime("%d.%m.%Y")), font=chart_number_font,
			color='black', fontsize=80, stroke_color='white',
			stroke_width=3, align='center',
		) \
			.set_duration(3) \
			.set_position(('center', 790)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		clip_site = mp.TextClip(
			txt='14:00-16:00 Fri.\neuropaplus.ru', font=text_font,
			color='white', fontsize=80, stroke_color='black',
			stroke_width=1, align='center',
		) \
			.set_duration(3) \
			.set_position((570, 100)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		clip_ep_logo = mp.ImageClip('package/ep_logo.png') \
			.set_duration(3) \
			.set_position((60, 70)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		return [
			clip_chart_number,
			clip_chart_date,
			clip_site,
			clip_ep_logo,
		]
