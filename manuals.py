from datetime import datetime

from model.entity.chart import Chart
from model.entity.song import Song
from model.repository.song_repository import SongRepository


def add_song_to_db(authors, name, clip_path, clip_start_sec, clip_end_sec):
	song_object = Song({
		'name': name,
		'authors': authors,
		'clip_path': clip_path,
		'clip_start_sec': clip_start_sec,
		'clip_end_sec': clip_end_sec,
	})
	song_object.save()


def save_path(song_id, path, start_sec, end_sec):
	song = SongRepository().get_song_by_id(song_id)
	song.clip_path = path
	song.clip_start_sec = start_sec
	song.clip_end_sec = end_sec
	song.save()



# clip_folder = 'D:\\Artyom\\Проекты\\Top Club Chart\\клипы чарта\\regulars\\'
# clip_name = 'Zerb & Sofiya Nzau - Mwaki (Tiësto Extended VIP Mix) [CYfw7CzqltM].mp4'
# path = clip_folder + clip_name
# song_id = 293
# start_sec = 2 * 60 + 35.5
# c_end_sec = 2 * 60 + 40.5
# save_path(song_id, path, start_sec, c_end_sec)
# print('Done!')

chart = Chart(data={
	'chart_number': 451,
	'chart_date': datetime(2024, 2, 3)
})
# print(chart.get_lcs().position)

song = SongRepository().get_song_by_id(291)
clip_params = {
	'clip_path': song.clip_path,
	'clip_start_time': song.clip_start_sec,
	'clip_end_time': song.clip_end_sec,
	'author': song.authors,
	'name': song.name,
	'position': 22,
	'lw': 22,
	'peak': 1,
	'weeks': 11,
	'moving': 'up',
	'show_stats': True,
	'result_name': chart.chart_date.strftime("%Y-%m-%d") + ' ' + str(22),
	'need_render': True,
	'is_lcs': True,
}
from clips.position import create_position_clip
create_position_clip(**clip_params)
