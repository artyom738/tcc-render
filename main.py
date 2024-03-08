import multiprocessing
import random
import os
from datetime import datetime
import moviepy.editor as mp
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from clips.position import create_position_clip, create_last_out_clip
from model.repository.song_repository import SongRepository
from model.entity.chart import Chart

intro_clip_path = 'package/intro.mp4'
after_intro_animation_path = 'package/tricolor3.mp4'
after_all_time_animation_path = 'package/rounds1.mp4'
after_outs_animation_path = 'package/round-arrow.mp4'
after_residance_animation_path = 'package/tricolor1.mp4'
after_positions_animation_path = 'package/tricolor2.mp4'
after_perspective_animation_path = 'package/rounds2.mp4'

all_time_label_path = 'package/alltime.avi'
residance_label_path = 'package/residance.avi'
perspective_label_path = 'package/perspective.avi'


def get_outro_path():
	number = random.randint(1, 3)
	return 'package/Outro TCC ' + str(number) + '.mp4'


def get_outro_audio():
	name = random.choice(os.listdir('D:/Artyom/Проекты/Python/tcc-render/package/outro'))
	return 'package/outro/' + name


def get_intro():
	intro_clip = mp.VideoFileClip(
		intro_clip_path,
		target_resolution=(1080, 1920)
	)
	return intro_clip


def get_after_intro_animation(total_duration: float):
	return mp.VideoFileClip(
		after_intro_animation_path,
		target_resolution=(1080, 1920)
	) \
		.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
		.set_start(total_duration - 25 / 30)


def get_all_time(song_id: int):
	song = SongRepository().get_song_by_id(song_id)
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
		'result_name': f'{chart.chart_number} (all time dance anthem)',
		'need_render': True,
		'is_lcs': False,
	}
	clip = create_position_clip(**clip_params)

	label = mp.VideoFileClip(
		all_time_label_path,
		target_resolution=(1080, 1920),
	) \
		.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
		.set_start(0.5)

	label_duration = label.duration
	label = label.set_fps(label.fps * label_duration / (clip.duration - 1))
	label = label.fx(vfx.speedx, label_duration / (clip.duration - 1))

	return mp.CompositeVideoClip([clip, label])


def get_after_all_time_animation(total_duration: float):
	animation = mp.VideoFileClip(
		after_all_time_animation_path,
		target_resolution=(1080, 1920)
	) \
		.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
		.set_start(total_duration - 28 / 30)

	return animation


def get_outs(total_duration: float, chart: Chart):
	song_repo = SongRepository()
	out_clip_list = []
	outs = chart.outs
	processes = []
	for index, out in enumerate(outs):
		song = song_repo.get_song_by_id(out.song_id)
		clip_times = song.get_clip_times()
		clip_params = {
			'clip_path': song.clip_path,
			'clip_start_time': clip_times['start_time'],
			'clip_end_time': clip_times['end_time'],
			'author': song.authors,
			'name': song.name,
			'position': 'OUT',
			'lw': out.get_lw(),
			'peak': song.get_peak(),
			'weeks': song.get_weeks(),
			'moving': None,
			'show_stats': True,
			'result_name': f'{chart.chart_number} out {str(index)}',
			'need_render': True,
		}
		if index == len(outs) - 1:
			clip_params['chart_date'] = chart.chart_date.strftime("%d.%m.%Y")
			clip_params['chart_number'] = chart.chart_number
			process = multiprocessing.Process(target=create_last_out_clip, kwargs=clip_params)
		else:
			process = multiprocessing.Process(target=create_position_clip, kwargs=clip_params)
		processes.append(process)
		process.start()

	[process.join() for process in processes]

	for index, out in enumerate(outs):
		song_clip = mp.VideoFileClip(
			filename=f'video_parts/{chart.chart_number} out {str(index)}.mp4'
		)
		out_clip_list.append(song_clip)
		print('Added out ' + str(index))

	if len(out_clip_list) > 0:
		return mp.concatenate_videoclips(out_clip_list).set_start(total_duration)
	else:
		print('Out list is empty')
		exit()


def get_after_outs_animation(total_duration: float):
	animation = mp.VideoFileClip(
		after_outs_animation_path,
		target_resolution=(1080, 1920)
	) \
		.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
		.set_start(total_duration - 25 / 30)

	return animation


def get_residance(song_id: int):
	song = SongRepository().get_song_by_id(song_id)
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
		'result_name': f'{chart.chart_number} (residance)',
		'need_render': True,
		'is_lcs': False,
	}
	clip = create_position_clip(**clip_params)

	label = mp.VideoFileClip(
		residance_label_path,
		target_resolution=(1080, 1920),
	) \
		.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
		.set_start(0.5)
	label_duration = label.duration
	label = label.set_fps(label.fps * label_duration / (clip.duration - 1))
	label = label.fx(vfx.speedx, label_duration / (clip.duration - 1))

	return mp.CompositeVideoClip([clip, label])


def get_after_residance_animation(total_duration: float):
	animation = mp.VideoFileClip(
		after_residance_animation_path,
		target_resolution=(1080, 1920)
	) \
		.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
		.set_start(total_duration - 25 / 30)

	return animation


def get_positions(total_duration: float, chart: Chart):
	song_repo = SongRepository()
	song_clip_list = []
	positions = chart.positions
	print('Chart date: ', chart.chart_date.strftime("%Y-%m-%d"))

	processes = []
	for index, position in enumerate(positions):
		song_id = position.song_id
		song = song_repo.get_song_by_id(song_id)
		clip_times = song.get_clip_times()
		clip_params = {
			'clip_path': song.clip_path,
			'clip_start_time': clip_times['start_time'],
			'clip_end_time': clip_times['end_time'],
			'author': song.authors,
			'name': song.name,
			'position': position.position,
			'lw': position.get_lw(),
			'peak': song.get_peak(),
			'weeks': song.get_weeks(),
			'moving': position.get_moving(),
			'show_stats': True,
			'result_name': f'{chart.chart_number} ({str(position.position)})',
			'need_render': True,
			'is_lcs': position.is_lcs,
		}
		process = multiprocessing.Process(target=create_position_clip, kwargs=clip_params)
		processes.append(process)
		process.start()

	[process.join() for process in processes]

	for index, position in enumerate(positions):
		song_clip = mp.VideoFileClip(
			filename=f'video_parts/{chart.chart_number} ({str(position.position)}).mp4'
		)
		song_clip_list.append(song_clip)
		print('Added position ' + str(position.position))

	songs_clip = mp.concatenate_videoclips(song_clip_list).set_start(total_duration)

	return songs_clip


def get_perspective(song_id: int):
	song = SongRepository().get_song_by_id(song_id)
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
		'result_name': f'{chart.chart_number} (perspective)',
		'need_render': True,
		'is_lcs': False,
	}
	clip = create_position_clip(**clip_params)

	label = mp.VideoFileClip(
		perspective_label_path,
		target_resolution=(1080, 1920),
	) \
		.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
		.set_start(0.5)
	label_duration = label.duration
	label = label.set_fps(label.fps * label_duration / (clip.duration - 1))
	label = label.fx(vfx.speedx, label_duration / (clip.duration - 1))

	return mp.CompositeVideoClip([clip, label])


def get_after_perspective_animation(total_duration: float):
	animation = mp.VideoFileClip(
		after_perspective_animation_path,
		target_resolution=(1080, 1920)
	) \
		.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
		.set_start(total_duration - 25 / 30)

	return animation


def get_outro(total_duration: float):
	outro_audio = mp.AudioFileClip(get_outro_audio()) \
		.audio_fadein(1) \
		.audio_fadeout(1) \
		.fx(afx.volumex, 0.5) \
		.set_start(total_duration)

	outro_clip = mp.VideoFileClip(
		get_outro_path(),
		target_resolution=(1080, 1920)
	) \
		.subclip(0, 11) \
		.fadeout(1) \
		.set_audio(outro_audio) \
		.set_start(total_duration)

	return outro_clip


def get_after_positions_animation(total_duration: float):
	return mp.VideoFileClip(
		after_positions_animation_path,
		target_resolution=(1080, 1920)
	) \
		.fx(vfx.mask_color, color=[0, 255, 0], s=5, thr=130) \
		.set_start(total_duration - 19 / 30)


def __main__(chart: Chart):
	current_time = datetime.now()
	print('Started at', current_time.strftime('%Y-%m-%d %H:%M:%S'))
	total_duration = 0
	intro_clip = get_intro()
	total_duration += intro_clip.duration
	after_intro_animation = get_after_intro_animation(total_duration)

	# All time dance anthem
	all_time_clip = get_all_time(chart.all_time_song_id)
	all_time_clip = all_time_clip.set_start(total_duration)
	total_duration += all_time_clip.duration
	after_all_time_animation = get_after_all_time_animation(total_duration)

	# Out clips
	outs_clip = get_outs(total_duration, chart)
	total_duration += outs_clip.duration
	after_outs_animation = get_after_outs_animation(total_duration)

	# Residance
	residance_clip = get_residance(chart.residance_song_id)
	residance_clip = residance_clip.set_start(total_duration)
	total_duration += residance_clip.duration
	after_residance_animation = get_after_residance_animation(total_duration)

	# Positions
	songs_clip = get_positions(total_duration, chart)
	total_duration += songs_clip.duration
	after_positions_animation = get_after_positions_animation(total_duration)

	# Perspective
	perspective_clip = get_perspective(chart.perspective_song_id)
	perspective_clip = perspective_clip.set_start(total_duration)
	total_duration += perspective_clip.duration
	after_perspective_animation = get_after_perspective_animation(total_duration)

	outro_clip = get_outro(total_duration)

	final = mp.CompositeVideoClip([
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

	final.write_videofile(f'production/tcc {chart.chart_date.strftime("%Y-%m-%d")}.mp4', fps=30, codec='mpeg4', bitrate='8000k', threads=8)
	# final.write_videofile('video_parts/tcc ' + chart.chart_date.strftime('%Y-%m-%d') + '.mp4', fps=10, codec='mpeg4', bitrate='200k', threads=8)

	print('Finished at', current_time.strftime('%Y-%m-%d %H:%M:%S'))
	seconds = (datetime.now() - current_time).total_seconds()
	print('Rendered by ', str(int(seconds // 60)), ' min ', str(int(seconds % 60)), ' sec')


if __name__ == '__main__':
	# Chart date format YYYY-MM-DD
	chart = Chart(data={
		'chart_number': 455,
		'chart_date': datetime(2024, 3, 2)
	})
	__main__(chart)
