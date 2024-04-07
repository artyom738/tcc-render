import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from moviepy.Clip import Clip

from charts.base_chart import BaseChart
from clips.position import chart_number_font, text_font


class Darknity(BaseChart):
	def get_chart_type(self) -> str:
		return 'dark'

	def get_position_text_color(self, position: int = 0):
		if position <= 5:
			return '#620572'  # Purple
		if position <= 10:
			return '#2fa83f'  # Light green
		if position <= 20:
			return '#126316'  # Dark green
		if position <= 30:
			return '#d8cd1b'  # Yellow
		if position <= 40:
			return '#c07126'  # Orange
		if position <= 50:
			return '#970b0a'  # Red
		return '#1566af'  # Blue

	def get_position_font_family(self) -> str:
		return 'Andes-Cnd-W04-SemiBold'

	def need_show_lcs(self):
		return False

	def get_last_out_composition(self) -> list[Clip]:
		clip_chart_number = mp.TextClip(
			txt=f'Darknity Top 50 #{self.chart.chart_number}', font=chart_number_font,
			color='#ed5126', fontsize=180, stroke_color='white',
			stroke_width=5, align='center',
		) \
			.set_duration(3) \
			.set_position(('center', 400)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		clip_chart_date = mp.TextClip(
			txt=str(self.chart.chart_date.strftime("%d.%m.%Y")), font=chart_number_font,
			color='#ffec8c', fontsize=100, stroke_color='black',
			stroke_width=3, align='center',
		) \
			.set_duration(3) \
			.set_position(('center', 790)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		clip_site = mp.TextClip(
			txt='18:00-20:00 Sat. on D1R Radio', font=text_font,
			color='white', fontsize=80, stroke_color='black',
			stroke_width=1, align='center',
		) \
			.set_duration(3) \
			.set_position(('center', 100)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		# clip_ep_logo = mp.ImageClip('package/ep_logo.png') \
		# 	.set_duration(3) \
		# 	.set_position((60, 70)) \
		# 	.crossfadein(0.4) \
		# 	.crossfadeout(0.4)

		return [
			clip_chart_number,
			clip_chart_date,
			clip_site,
			# clip_ep_logo,
		]
