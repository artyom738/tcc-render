import moviepy.editor as mp

intro_clip_path = 'D:\\Artyom\\Проекты\\Sony Vegas 13\\интро ткч видео1.mp4'
after_intro_animation_path = 'D:\\Artyom\\Проекты\\Top Club Chart\\переходы\\триколор3.mp4'
after_past_animation_path = 'D:\\Artyom\\Проекты\\Top Club Chart\\переходы\\круг стрелка.mp4'


def create_intro(chart_date=None, chart_number=None):
	intro_clip = mp.VideoFileClip(intro_clip_path)

	clip_list = [
		intro_clip,
	]

	final = mp.CompositeVideoClip(clip_list)
	final.write_videofile("video_parts/intro.mp4", fps=30, codec='mpeg4', bitrate="8000k")



