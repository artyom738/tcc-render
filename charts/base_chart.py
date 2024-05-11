from datetime import datetime
import librosa
import moviepy.editor as mp
import multiprocessing
import numpy as np
import random
import os
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from moviepy.Clip import Clip

from clips.position import create_position_clip, create_last_out_clip
from model.repository.song_repository import SongRepository
from model.entity.chart import Chart


class BaseChart:
	def __init__(self, chart: Chart):
		self.chart = chart
		self.song_repo: SongRepository = SongRepository()

	def get_chart_type(self) -> str:
		raise NotImplementedError

	def get_last_out_composition(self) -> list[Clip]:
		return []

	def get_position_text_color(self, position: int = 0) -> str:
		return '#36c2f8'

	def get_position_font_family(self) -> str:
		return 'Microsoft-PhagsPa-Bold'

	def get_intro(self):
		return mp.VideoFileClip(
			'package/' + self.get_chart_type() + '/intro.mp4',
			target_resolution=(1080, 1920)
		)

	def get_outro_audio(self):
		name = random.choice(os.listdir('package/outro'))
		return 'package/outro/' + name

	def get_outro_path(self):
		number = random.randint(1, 3)
		return 'package/Outro TCC ' + str(number) + '.mp4'

	def get_after_intro_animation(self, total_duration: float):
		return mp.VideoFileClip(
			'package/tricolor3.mp4',
			target_resolution=(1080, 1920)
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(total_duration - 25 / 30)

	def get_outs(self, total_duration: float, chart: Chart):
		out_clip_list = []
		outs = chart.outs
		processes = []
		for index, out in enumerate(outs):
			song = self.song_repo.get_song_by_id(out.song_id)
			clip_times = song.get_clip_times()
			clip_params = {
				'clip_path': song.clip_path,
				'clip_start_time': clip_times['start_time'],
				'clip_end_time': clip_times['end_time'],
				'author': song.authors,
				'name': song.name,
				'position': 'OUT',
				'lw': out.get_lw(),
				'peak': song.get_peak(self.get_chart_type(), self.chart.chart_date),
				'weeks': song.get_weeks(self.get_chart_type(), self.chart.chart_date),
				'moving': None,
				'show_stats': True,
				'result_name': f'{chart.chart_type}/{chart.chart_number}/out {str(index)}',
				'need_render': True,
				'chart': self,
				'position_text_color': self.get_position_text_color(),
				'position_font_family': self.get_position_font_family(),
			}
			if index == len(outs) - 1:
				clip_params['chart_date'] = chart.chart_date.strftime("%d.%m.%Y")
				clip_params['chart_number'] = chart.chart_number
				process = multiprocessing.Process(target=create_last_out_clip, kwargs={'params': clip_params})
			else:
				process = multiprocessing.Process(target=create_position_clip, kwargs={'params': clip_params})
			processes.append(process)
			process.start()

		[process.join() for process in processes]

		for index, out in enumerate(outs):
			filename = f'video_parts/{chart.chart_type}/{chart.chart_number}/out {str(index)}.mp4'
			song_clip = mp.VideoFileClip(
				filename=filename
			)
			# Applying volume changing to get average amplitude 0.3
			etalon_amplidude = 0.3
			y, sr = librosa.load(filename)
			amplitude_envelope = librosa.feature.rms(y=y)[0]
			average_amplitude = round(np.mean(amplitude_envelope), 2)
			song_clip = song_clip.fx(afx.volumex, etalon_amplidude / average_amplitude)
			print(f'Multiplied by {etalon_amplidude / average_amplitude}')
			out_clip_list.append(song_clip)
			print('Added out ' + str(index))

		if len(out_clip_list) > 0:
			return mp.concatenate_videoclips(out_clip_list).set_start(total_duration)
		else:
			print('Out list is empty')

	def get_after_outs_animation(self, total_duration: float):
		animation = mp.VideoFileClip(
			'package/round-arrow.mp4',
			target_resolution=(1080, 1920)
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(total_duration - 25 / 30)

		return animation

	def need_show_lcs(self):
		return True

	def get_positions(self, total_duration: float, chart: Chart):
		song_clip_list = []
		positions = chart.positions
		print('Chart date: ', chart.chart_date.strftime("%Y-%m-%d"))

		processes = []
		for index, position in enumerate(positions):
			song_id = position.song_id
			song = self.song_repo.get_song_by_id(song_id)
			clip_times = song.get_clip_times()
			clip_params = {
				'clip_path': song.clip_path,
				'clip_start_time': clip_times['start_time'],
				'clip_end_time': clip_times['end_time'],
				'author': song.authors,
				'name': song.name,
				'position': position.position,
				'lw': position.get_lw(),
				'peak': song.get_peak(self.get_chart_type(), self.chart.chart_date),
				'weeks': song.get_weeks(self.get_chart_type(), self.chart.chart_date),
				'moving': position.get_moving(),
				'show_stats': True,
				'result_name': f'{chart.chart_type}/{chart.chart_number}/{str(position.position)}',
				'need_render': True,
				'is_lcs': self.need_show_lcs() & position.is_lcs,
				'position_text_color': self.get_position_text_color(position.position),
				'position_font_family': self.get_position_font_family(),
			}
			process = multiprocessing.Process(target=create_position_clip, kwargs={'params': clip_params})
			processes.append(process)
			process.start()

		[process.join() for process in processes]

		for index, position in enumerate(positions):
			filename = f'video_parts/{chart.chart_type}/{chart.chart_number}/{str(position.position)}.mp4'
			song_clip = mp.VideoFileClip(
				filename=filename
			)

			# Applying volume changing to get average amplitude 0.3
			etalon_amplidude = 0.3
			y, sr = librosa.load(filename)
			amplitude_envelope = librosa.feature.rms(y=y)[0]
			average_amplitude = round(np.mean(amplitude_envelope), 2)
			song_clip = song_clip.fx(afx.volumex, etalon_amplidude / average_amplitude)
			print(f'Multiplied by {etalon_amplidude / average_amplitude}')

			song_clip_list.append(song_clip)
			print('Added position ' + str(position.position))

		songs_clip = mp.concatenate_videoclips(song_clip_list).set_start(total_duration)

		return songs_clip

	def get_after_positions_animation(self, total_duration: float):
		return mp.VideoFileClip(
			'package/tricolor2.mp4',
			target_resolution=(1080, 1920)
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(total_duration - 19 / 30)

	def get_outro(self, total_duration: float):
		outro_audio = mp.AudioFileClip(self.get_outro_audio()) \
			.audio_fadein(1) \
			.audio_fadeout(1) \
			.fx(afx.volumex, 0.5) \
			.set_start(total_duration)

		outro_clip = mp.VideoFileClip(
			self.get_outro_path(),
			target_resolution=(1080, 1920)
		) \
			.subclip(0, 11) \
			.fadeout(1) \
			.set_audio(outro_audio) \
			.set_start(total_duration)

		return outro_clip

	def generate_clip(self):
		total_duration = 0

		# Intro
		intro_clip = self.get_intro()
		total_duration += intro_clip.duration
		after_intro_animation = self.get_after_intro_animation(total_duration)

		# Out clips
		outs_clip = self.get_outs(total_duration, self.chart)
		total_duration += outs_clip.duration
		after_outs_animation = self.get_after_outs_animation(total_duration)

		# Positions
		songs_clip = self.get_positions(total_duration, self.chart)
		total_duration += songs_clip.duration
		after_positions_animation = self.get_after_positions_animation(total_duration)

		outro_clip = self.get_outro(total_duration)

		return mp.CompositeVideoClip([
			intro_clip,
			outs_clip,
			songs_clip,
			outro_clip,
			after_intro_animation,
			after_outs_animation,
			after_positions_animation,
		]) \
			# .subclip(47, 47.2)

	def render(self):
		tmp_clip_path = f'video_parts/{self.chart.chart_type}/{self.chart.chart_number}'
		if not os.path.exists(tmp_clip_path):
			os.makedirs(tmp_clip_path)
		current_time = datetime.now()
		print('Started at', current_time.strftime('%Y-%m-%d %H:%M:%S'))
		final = self.generate_clip()
		final.write_videofile(
			f'production/{self.get_chart_type()} {self.chart.chart_date.strftime("%Y-%m-%d")}.mp4',
			fps=30,
			codec='mpeg4',
			bitrate='8000k',
			threads=8,
		)
		# final.write_videofile('video_parts/tcc ' + chart.chart_date.strftime('%Y-%m-%d') + '.mp4', fps=10, codec='mpeg4', bitrate='200k', threads=8)

		print('Finished at', current_time.strftime('%Y-%m-%d %H:%M:%S'))
		seconds = (datetime.now() - current_time).total_seconds()
		print('Rendered by ', str(int(seconds // 60)), ' min ', str(int(seconds % 60)), ' sec')
