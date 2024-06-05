import librosa
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from moviepy.Clip import Clip
import numpy as np

from charts.base_chart import BaseChart
from clips.position import chart_number_font, text_font, create_position_clip


class Eht40(BaseChart):
	def get_chart_type(self) -> str:
		return 'eht'

	def get_position_text_color(self, position: int = 0):
		if position <= 5:
			return '#ed9b2b'  # Orange
		return '#1566af'  # Blue

	def need_save_preview(self) -> bool:
		return True

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

		label = mp.VideoFileClip(
			'package/eht/eht_old.avi',
			target_resolution=(1080, 1920),
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(0.5)
		label_duration = label.duration
		label = label.set_fps(label.fps * label_duration / (clip.duration - 1))
		label = label.fx(vfx.speedx, label_duration / (clip.duration - 1))

		return mp.CompositeVideoClip([clip, label])

	def get_after_old_animation(self, total_duration: float):
		animation = mp.VideoFileClip(
			'package/rounds1.mp4',
			target_resolution=(1080, 1920)
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(total_duration - 28 / 30)

		return animation

	def get_perspective_clip(self, song_id: int):
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
			'result_name': f'{self.chart.chart_type}/{self.chart.chart_number}/perspective',
			'need_render': True,
			'is_lcs': False,
		}
		clip = create_position_clip(clip_params)

		# Applying volume changing to get average amplitude 0.3
		etalon_amplidude = 0.3
		y, sr = librosa.load(f'video_parts/{self.chart.chart_type}/{self.chart.chart_number}/perspective.mp4')
		amplitude_envelope = librosa.feature.rms(y=y)[0]
		average_amplitude = round(np.mean(amplitude_envelope), 2)
		clip = clip.fx(afx.volumex, etalon_amplidude / average_amplitude)
		print(f'Multiplied by {etalon_amplidude / average_amplitude}')

		label = mp.VideoFileClip(
			'package/eht/eht_perspective.avi',
			target_resolution=(1080, 1920),
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(0.5)
		label_duration = label.duration
		label = label.set_fps(label.fps * label_duration / (clip.duration - 1))
		label = label.fx(vfx.speedx, label_duration / (clip.duration - 1))

		return mp.CompositeVideoClip([clip, label])

	def get_after_perspective_animation(self, total_duration: float):
		animation = mp.VideoFileClip(
			'package/rounds1.mp4',
			target_resolution=(1080, 1920)
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(total_duration - 28 / 30)

		return animation

	def generate_clip(self):
		total_duration = 0
		intro_clip = self.get_intro()
		total_duration += intro_clip.duration
		after_intro_animation = self.get_after_intro_animation(total_duration)

		# Out clips
		outs_clip = self.get_outs(total_duration, self.chart)
		total_duration += outs_clip.duration
		after_outs_animation = self.get_after_outs_animation(total_duration)

		# Сегодня завтра вчера
		old_clip = self.get_old_clip(self.chart.rubric['eht_old_song_id'])
		old_clip = old_clip.set_start(total_duration)
		total_duration += old_clip.duration
		after_old_clip_animation = self.get_after_old_animation(total_duration)

		# Positions
		songs_clip = self.get_positions(total_duration, self.chart)
		total_duration += songs_clip.duration
		after_positions_animation = self.get_after_positions_animation(total_duration)

		# Взгляд в будущее
		perspective_clip = self.get_perspective_clip(self.chart.rubric['eht_perspective_song_id'])
		perspective_clip = perspective_clip.set_start(total_duration)
		total_duration += perspective_clip.duration
		after_perspective_animation = self.get_after_perspective_animation(total_duration)

		outro_clip = self.get_outro(total_duration)

		return mp.CompositeVideoClip([
			intro_clip,
			outs_clip,
			old_clip,
			songs_clip,
			perspective_clip,
			outro_clip,
			after_intro_animation,
			after_old_clip_animation,
			after_outs_animation,
			after_positions_animation,
			after_perspective_animation,
		]) \
			# .subclip(47, 47.2)
