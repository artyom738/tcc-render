from chorus_finder.v1 import ChorusFinderV1
from chorus_finder.v2 import ChorusFinderV2
from chorus_finder.v3 import ChorusFinderV3

from model.entity.song import Song
from model.repository.song_repository import song_repository


class ChorusFinder:
	def get_chorus_finder(self, chorus_finder_version: int):
		if chorus_finder_version == 1:
			return ChorusFinderV1()
		if chorus_finder_version == 2:
			return ChorusFinderV2()
		if chorus_finder_version == 3:
			return ChorusFinderV3()

	def analyze_track(self, audio_path: str, draw_chart=False, find_times=True):
		result = self.get_chorus_finder(3).find_chorus(audio_path, draw_chart, find_times)

		return result

	# Analyses song and fills row in db.
	def fill_song_info(self, song: Song):
		if song.clip_path and not song.clip_start_sec and not song.clip_end_sec:
			result = self.analyze_track(song.clip_path)
			song \
				.set_clip_start_sec(result['start_times']) \
				.set_clip_end_sec(result['end_times']) \
				.save()
			print(f'Analysing song {song.id} was finished')

	def reanalyze_songs(self, min_id: int = 0):
		songs = song_repository.get_by_greater_id(min_id)
		for song in songs:
			self.fill_song_info(song)

	def reanalyze_song(self, song_id: int):
		song = song_repository.get_song_by_id(song_id)
		self.fill_song_info(song)

	def debug_analyzing(self, song_id: int):
		song = song_repository.get_song_by_id(song_id)
		finder = ChorusFinderV3()
		result = finder.find_chorus(song.clip_path, draw_chart=True, find_times=True)
		print(result)


if __name__ == '__main__':
	# ChorusFinder().debug_analyzing(677)
	ChorusFinder().reanalyze_song(904)
	# ChorusFinder().reanalyze_songs()
