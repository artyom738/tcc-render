from charts.list import List
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from moviepy.Clip import Clip
import numpy as np
from datetime import datetime, date
from clips.position import chart_number_font, text_font, create_position_clip
import librosa

from charts.base_chart import BaseChart
from clips.position import chart_number_font, text_font


class EhtNy(List):
	def get_intro(self):
		#  May be changed due to variable charts
		return mp.VideoFileClip(
			'package/eht/intro-ny.mp4',
			target_resolution=(1080, 1920)
		)

	def get_after_old_animation(self, total_duration: float):
		animation = mp.VideoFileClip(
			'package/rounds1.mp4',
			target_resolution=(1080, 1920)
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(total_duration - 28 / 30)

		return animation

	def get_additional_stat_info(self, song: 'Song'):
		return None

	def get_old_clip(self, song_id: int):
		song = self.song_repo.get_song_by_id(song_id)
		clip_times = song.get_clip_times()
		clip_params = {
			'clip_path': song.clip_path,
			'clip_start_time': clip_times['start_time'],
			'clip_end_time': clip_times['end_time'],
			'author': song.authors,
			'name': song.name,
			'position': None,
			'lw': None,
			'peak': None,
			'weeks': None,
			'moving': None,
			'show_stats': False,
			'result_name': f'{self.chart.chart_type}/{self.chart.chart_number}/old',
			'need_render': True,
			'is_lcs': False,
		}
		clip = create_position_clip(clip_params)

		# Applying volume changing to get average amplitude 0.3
		etalon_amplidude = 0.3
		y, sr = librosa.load(f'video_parts/{self.chart.chart_type}/{self.chart.chart_number}/old.mp4')
		amplitude_envelope = librosa.feature.rms(y=y)[0]
		average_amplitude = round(np.mean(amplitude_envelope), 2)
		clip = clip.fx(afx.volumex, etalon_amplidude / average_amplitude)
		print(f'Multiplied by {etalon_amplidude / average_amplitude}')

		label = mp.TextClip(
			txt='Лидер в 2023 году',
			font=text_font,
			color='white',
			fontsize=70,
			stroke_color='black',
			stroke_width=2,
			align='West',
		).set_duration(clip.duration).set_position((60, 60))

		return mp.CompositeVideoClip([clip, label])

	def generate_clip(self):
		total_duration = 0
		intro_clip = self.get_intro()
		total_duration += intro_clip.duration
		after_intro_animation = self.get_after_intro_animation(total_duration)

		# Прошлогодний
		old_clip = self.get_old_clip(self.chart.rubric['eht_old_song_id'])
		old_clip = old_clip.set_start(total_duration)
		total_duration += old_clip.duration
		after_old_clip_animation = self.get_after_old_animation(total_duration)

		songs_clip = self.get_positions(total_duration, self.chart)

		total_duration += songs_clip.duration
		after_perspective_animation = self.get_after_perspective_animation(total_duration)
		outro_clip = self.get_outro(total_duration)

		return mp.CompositeVideoClip([
			intro_clip,
			old_clip,
			songs_clip,
			outro_clip,
			after_intro_animation,
			after_perspective_animation,
			after_old_clip_animation,
		]) \
			# .subclip(47, 47.2)
