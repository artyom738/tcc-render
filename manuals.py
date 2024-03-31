from datetime import datetime

from moviepy.video.VideoClip import TextClip

from model.entity.chart import Chart
from model.entity.song import Song
from model.repository.song_repository import SongRepository

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

print(TextClip.list('font'))
