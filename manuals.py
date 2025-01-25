from datetime import datetime

from moviepy.video.VideoClip import TextClip
from datetime import datetime
import librosa
import moviepy.editor as mp
import multiprocessing
import concurrent.futures
import numpy as np
import random
import os
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
from moviepy.Clip import Clip
from yt_dlp import YoutubeDL

from clips.position import create_position_clip, create_last_out_clip
from model.repository.song_repository import song_repository

from model.entity.chart import Chart
from model.entity.song import Song
from model.repository.song_repository import song_repository

# chart = Chart(data={
# 	'chart_number': 451,
# 	'chart_date': datetime(2024, 2, 3),
# 	'chart_type': 'tcc',
# })

# song = SongRepository('tcc').get_song_by_id(291)
# clip_params = {
# 	'clip_path': song.clip_path,
# 	'clip_start_time': song.clip_start_sec,
# 	'clip_end_time': song.clip_end_sec,
# 	'author': song.authors,
# 	'name': song.name,
# 	'position': 22,
# 	'lw': 22,
# 	'peak': 1,
# 	'weeks': 11,
# 	'moving': 'up',
# 	'show_stats': True,
# 	'result_name': chart.chart_date.strftime("%Y-%m-%d") + ' ' + str(22),
# 	'need_render': True,
# 	'is_lcs': True,
# }
from clips.position import create_position_clip
# create_position_clip(**clip_params)


city_video_path = 'package/city.mp4'
from skimage.filters import gaussian
import moviepy.editor as mp

def blur(image):
	return gaussian(image.astype(float), sigma=10, channel_axis=-1)

# bg_video = mp.VideoFileClip(city_video_path, target_resolution=(1080, 1920)).subclip(10, 20*60).fl_image(blur)
# bg_video.write_videofile('video_parts/city_blur1.mp4', fps=24, codec='mpeg4', bitrate='3000k', threads=16)

# print(TextClip.list('font'))


def recode(clip_path: str):
	YoutubeDL.encode()


if __name__ == '__main__':
	filename = f'video_parts/tcc/495/6.mp4'
	song_clip = mp.VideoFileClip(
		filename=filename
	)
	# Applying volume changing to get average amplitude 0.3
	etalon_amplidude = 0.3
	y, sr = librosa.load(filename)
	amplitude_envelope = librosa.feature.rms(y=y)[0]
	average_amplitude = round(np.mean(amplitude_envelope), 2)
	song_clip = song_clip.fx(afx.volumex, etalon_amplidude / average_amplitude)
	print(average_amplitude)
