import random

import moviepy.editor as mp
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from skimage.filters import gaussian
import os.path

# Fira-Sans-Extra-Condensed-SemiBold
# Roboto-Condensed-Bold
text_font = 'Fira-Sans-Extra-Condensed-SemiBold'

number_font = 'Microsoft-PhagsPa-Bold'
# Andes-Cnd-W04-SemiBold
# Microsoft-PhagsPa-Bold
# Bakbak-One-Regular

chart_number_font = 'GraphikLCG-BlackItalic'
city_video_path = 'package/city_blur1.mp4'


def create_position_clip(params: dict):
	clip_path = params.get('clip_path', None)
	if not params.get('clip_path'):
		raise Exception('Clip path for render is None')

	clip_start_time = params.get('clip_start_time', 0)
	clip_end_time = params.get('clip_end_time', 4)
	author = params.get('author', 'Noname')
	name = params.get('name', 'Untitled')
	position = params.get('position', '44')
	lw = params.get('lw', '44')
	peak = params.get('peak', '44')
	weeks = params.get('weeks', '44')
	moving = params.get('moving', 'up')
	show_stats = params.get('show_stats', True)
	result_name = params.get('result_name', 'rendered_clip')
	is_lcs = params.get('is_lcs', False)
	additional_stat = params.get('additional_stat', None)
	need_render = params.get('need_render', False)
	position_text_color = params.get('position_text_color', '#781fdb')
	position_font_family = params.get('position_font_family', 'Microsoft-PhagsPa-Bold')

	if need_render and os.path.isfile('video_parts/' + result_name + '.mp4'):
		return mp.VideoFileClip(filename='video_parts/' + result_name + '.mp4')

	clip1 = mp.VideoFileClip(clip_path)
	music_clip = clip1.subclip(clip_start_time, clip_end_time).resize(height=1080)
	duration = music_clip.duration
	clip_width, clip_height = music_clip.size

	background_video = None
	if clip_width == clip_height:
		bg_video = mp.VideoFileClip(city_video_path, target_resolution=(1080, 1920))
		bg_start_time = random.random() * bg_video.duration * 0.9
		bg_end_time = bg_start_time + duration
		background_video = bg_video.subclip(bg_start_time, bg_end_time)
		start_size = 0.85
		end_size = 0.9
		music_clip = music_clip \
			.set_position(('center', 'center')) \
			.resize(start_size) \
			.resize(lambda t: 1 + (end_size - start_size) / (start_size * duration) * t)
	elif clip_width != 1920:
		background_video = mp.ColorClip(size=(1920, 1080), color=[0, 0, 0], duration=duration)
		music_clip = music_clip.set_position(('center', 'center'))

	w, h = 1920, 1080

	clip_name = mp.TextClip(
		txt=author + "\n" + name,
		font=text_font,
		color='black',
		fontsize=84,
		stroke_color='white',
		stroke_width=2,
		align='West',
	).set_duration(duration).set_position((260, h - 280))

	clip_position = None
	if position:
		clip_position = mp.TextClip(
			txt=str(position),
			font=position_font_family,
			color=position_text_color,
			fontsize=220,
			stroke_color='white',
			stroke_width=2,
			align='center',
		).set_duration(duration).set_position((100, 70))

	clip_stats = None
	clip_lcs = None
	additional_stat_clip = None
	if show_stats:
		if lw is not None:
			stat_text = "Было: #" + str(lw) + " | Пик: #" + str(peak) + " | Недель: " + str(weeks)
		else:
			stat_text = "Пик: #" + str(peak) + " | Недель: " + str(weeks)

		clip_stats = mp.TextClip(
			txt=stat_text,
			font=text_font,
			color='white',
			fontsize=60,
			stroke_color='black',
			stroke_width=2,
			align='East',
		).set_duration(3)
		stats_width = clip_stats.size[0]
		clip_stats = clip_stats.set_position((w - stats_width - 60, 60))

		if is_lcs:
			clip_lcs = mp.TextClip(
				txt="Долгожитель чарта",
				font=text_font,
				color='red',
				fontsize=54,
				stroke_color='black',
				stroke_width=2,
				align='East',
			).set_duration(3)
			stats_width = clip_lcs.size[0]
			clip_lcs = clip_lcs.set_position((w - stats_width - 60, 135))

		if additional_stat:
			additional_stat_clip = mp.TextClip(
				txt=additional_stat,
				font=text_font,
				color='white',
				fontsize=60,
				stroke_color='black',
				stroke_width=2,
				align='East',
			).set_duration(3)
			stats_width = additional_stat_clip.size[0]
			additional_stat_clip = additional_stat_clip.set_position((w - stats_width - 60, 135))

	arrow_path = None
	if moving == 'up':
		arrow_path = 'package/arrow-up.png'
	elif moving == 'down':
		arrow_path = 'package/arrow-down.png'
	elif moving == 'same':
		arrow_path = 'package/arrow-same.png'
	elif moving == 'new':
		arrow_path = 'package/arrow-new.png'
	elif moving == 'double-down':
		arrow_path = 'package/arrow-double-down.png'
	elif moving == 'double-up':
		arrow_path = 'package/arrow-double-up.png'

	arrow = None
	if arrow_path:
		arrow = mp.ImageClip(arrow_path).set_duration(3)

	tcc_logo = mp.ImageClip(
		img='package/logo.jpg'
	).set_duration(duration).set_position((w - 280, h - 280))

	clip_list = [
		music_clip,
		clip_name.crossfadein(0.4).crossfadeout(0.4),
		tcc_logo,
	]
	if background_video:
		clip_list.insert(0, background_video)
	if arrow_path and arrow:
		clip_list.append(arrow.set_start(duration - 3).crossfadein(0.4).crossfadeout(0.4))
	if show_stats and clip_stats:
		clip_list.append(clip_stats.set_start(duration - 3).crossfadein(0.4).crossfadeout(0.4))
	if show_stats and is_lcs and clip_lcs:
		clip_list.append(clip_lcs.set_start(duration - 3).crossfadein(0.4).crossfadeout(0.4))
	if show_stats and not is_lcs and additional_stat and additional_stat_clip:
		clip_list.append(additional_stat_clip.set_start(duration - 3).crossfadein(0.4).crossfadeout(0.4))
	if position and clip_position:
		clip_list.append(clip_position.crossfadein(0.4).crossfadeout(0.4))

	final = mp.CompositeVideoClip(clip_list)

	if need_render:
		final.write_videofile('video_parts/' + result_name + '.mp4', fps=30, codec='mpeg4', bitrate='8000k')

	return final


def blur(image):
	return gaussian(image.astype(float), sigma=10, channel_axis=-1)


def create_last_out_clip(params: dict):
	clip_path = params.get('clip_path', None)
	if not params.get('clip_path'):
		raise Exception('Clip path for render is None')

	clip_start_time = params.get('clip_start_time', 0)
	clip_end_time = params.get('clip_end_time', 4)
	author = params.get('author', 'Noname')
	name = params.get('name', 'Untitled')
	position = params.get('position', '44')
	lw = params.get('lw', '44')
	peak = params.get('peak', '44')
	weeks = params.get('weeks', '44')
	moving = params.get('moving', 'up')
	show_stats = params.get('show_stats', True)
	result_name = params.get('result_name', 'rendered_clip')
	chart = params.get('chart', None)
	need_render = params.get('need_render', False)
	need_save_preview = params.get('need_save_preview', False)

	if need_render and os.path.isfile('video_parts/' + result_name + '.mp4'):
		return mp.VideoFileClip(filename='video_parts/' + result_name + '.mp4')

	position_params = {**params, 'clip_end_time': clip_end_time - 2}
	clip = create_position_clip(position_params)

	music_clip = mp.VideoFileClip(clip_path) \
		.subclip(clip_end_time - 2.2, clip_end_time + 1) \
		.fl_image(blur)
	music_clip = music_clip.resize(height=1080)
	duration = music_clip.duration
	clip_width, clip_height = music_clip.size

	background_video = None
	if clip_width == clip_height:
		bg_video = mp.VideoFileClip(city_video_path, target_resolution=(1080, 1920))
		bg_start_time = random.random() * bg_video.duration * 0.9
		bg_end_time = bg_start_time + duration
		background_video = bg_video.subclip(bg_start_time, bg_end_time)
		start_size = 0.9
		end_size = 0.87
		music_clip = music_clip \
			.set_position(('center', 'center')) \
			.resize(start_size) \
			.resize(lambda t: 1 + (end_size - start_size) / (start_size * duration) * t)
	elif clip_width != 1920:
		background_video = mp.ColorClip(size=(1920, 1080), color=[0, 0, 0], duration=duration)
		music_clip = music_clip.set_position(('center', 'center'))

	clip_list = [
		music_clip,
	] + chart.get_last_out_composition()
	if background_video:
		clip_list.insert(0, background_video)
	blurred_clip = mp.CompositeVideoClip(clip_list)

	final = mp.CompositeVideoClip([
		clip.fx(afx.audio_fadeout, 0.2),
		blurred_clip.crossfadein(0.2).set_start(clip.duration - 0.2).fx(afx.audio_fadein, 0.2)
	])

	if need_save_preview:
		preview_position = blurred_clip.duration / 2
		preview_name = f'previews/preview_{chart.chart.chart_type}_{chart.chart.chart_number}.png'
		blurred_clip.save_frame(preview_name, t=preview_position)
		print(f'Preview saved: {preview_name}')

	if need_render:
		final.write_videofile('video_parts/' + result_name + '.mp4', fps=30, codec='mpeg4', bitrate='8000k')

	return final
