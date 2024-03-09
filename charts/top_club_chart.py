import moviepy.editor as mp
import moviepy.video.fx.all as vfx
from moviepy.Clip import Clip

from charts.base_chart import BaseChart
from clips.position import create_position_clip, chart_number_font, text_font


class TopClubChart(BaseChart):
	all_time_label_path = 'package/alltime.avi'
	residance_label_path = 'package/residance.avi'
	perspective_label_path = 'package/perspective.avi'

	def get_chart_type(self):
		return 'tcc'

	def get_last_out_composition(self) -> list[Clip]:
		clip_chart_number = mp.TextClip(
			txt='#' + str(self.chart.chart_number), font=chart_number_font,
			color='#781fdb', fontsize=350, stroke_color='white',
			stroke_width=5, align='center',
		) \
			.set_duration(3) \
			.set_position((200, 400)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		clip_chart_date = mp.TextClip(
			txt=str(self.chart.chart_date.strftime("%d.%m.%Y")), font=chart_number_font,
			color='black', fontsize=80, stroke_color='white',
			stroke_width=3, align='center',
		) \
			.set_duration(3) \
			.set_position((1220, 790)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		clip_logo = mp.ImageClip('package/logo_large.jpg') \
			.set_duration(3) \
			.set_position((1200, 200)) \
			.crossfadein(0.4) \
			.crossfadeout(0.4)

		clip_site = mp.TextClip(
			txt='20:00-22:00 Sat.\neuropaplus.ru', font=text_font,
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
			clip_logo,
			clip_site,
			clip_ep_logo,
		]

	def get_all_time(self, song_id: int):
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
			'result_name': f'{self.chart.chart_number} (all time dance anthem)',
			'need_render': True,
			'is_lcs': False,
		}
		clip = create_position_clip(**clip_params)

		label = mp.VideoFileClip(
			'package/tcc/alltime.avi',
			target_resolution=(1080, 1920),
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(0.5)

		label_duration = label.duration
		label = label.set_fps(label.fps * label_duration / (clip.duration - 1))
		label = label.fx(vfx.speedx, label_duration / (clip.duration - 1))

		return mp.CompositeVideoClip([clip, label])

	def get_after_all_time_animation(self, total_duration: float):
		animation = mp.VideoFileClip(
			'package/rounds1.mp4',
			target_resolution=(1080, 1920)
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(total_duration - 28 / 30)

		return animation

	def get_residance(self, song_id: int):
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
			'result_name': f'{self.chart.chart_number} (residance)',
			'need_render': True,
			'is_lcs': False,
		}
		clip = create_position_clip(**clip_params)

		label = mp.VideoFileClip(
			'package/tcc/residance.avi',
			target_resolution=(1080, 1920),
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(0.5)
		label_duration = label.duration
		label = label.set_fps(label.fps * label_duration / (clip.duration - 1))
		label = label.fx(vfx.speedx, label_duration / (clip.duration - 1))

		return mp.CompositeVideoClip([clip, label])

	def get_after_residance_animation(self, total_duration: float):
		animation = mp.VideoFileClip(
			'package/tricolor1.mp4',
			target_resolution=(1080, 1920)
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(total_duration - 25 / 30)

		return animation

	def get_perspective(self, song_id: int):
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
			'result_name': f'{self.chart.chart_number} (perspective)',
			'need_render': True,
			'is_lcs': False,
		}
		clip = create_position_clip(**clip_params)

		label = mp.VideoFileClip(
			'package/tcc/perspective.avi',
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
			'package/rounds2.mp4',
			target_resolution=(1080, 1920)
		) \
			.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
			.set_start(total_duration - 25 / 30)

		return animation

	def generate_clip(self):
		total_duration = 0
		intro_clip = self.get_intro()
		total_duration += intro_clip.duration
		after_intro_animation = self.get_after_intro_animation(total_duration)

		# All time dance anthem
		all_time_clip = self.get_all_time(self.chart.all_time_song_id)
		all_time_clip = all_time_clip.set_start(total_duration)
		total_duration += all_time_clip.duration
		after_all_time_animation = self.get_after_all_time_animation(total_duration)

		# Out clips
		outs_clip = self.get_outs(total_duration, self.chart)
		total_duration += outs_clip.duration
		after_outs_animation = self.get_after_outs_animation(total_duration)

		# Residance
		residance_clip = self.get_residance(self.chart.residance_song_id)
		residance_clip = residance_clip.set_start(total_duration)
		total_duration += residance_clip.duration
		after_residance_animation = self.get_after_residance_animation(total_duration)

		# Positions
		songs_clip = self.get_positions(total_duration, self.chart)
		total_duration += songs_clip.duration
		after_positions_animation = self.get_after_positions_animation(total_duration)

		# Perspective
		perspective_clip = self.get_perspective(self.chart.perspective_song_id)
		perspective_clip = perspective_clip.set_start(total_duration)
		total_duration += perspective_clip.duration
		after_perspective_animation = self.get_after_perspective_animation(total_duration)

		outro_clip = self.get_outro(total_duration)

		return mp.CompositeVideoClip([
			intro_clip,
			all_time_clip,
			outs_clip,
			residance_clip,
			songs_clip,
			perspective_clip,
			outro_clip,
			after_intro_animation,
			after_all_time_animation,
			after_outs_animation,
			after_residance_animation,
			after_positions_animation,
			after_perspective_animation,
		]) \
			# .subclip(47, 47.2)
