import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from model.entity.song import Song
from model.repository.song_repository import SongRepository

matplotlib.use('TkAgg')


def analyze_track(audio_path: str, draw_chart=False, find_times=True):
	# Load audio file
	# audio_path = 'test_results/!York - On The Beach (Kryder Remix).mp3'
	result = dict()
	y, sr = librosa.load(audio_path)
	full_duration = librosa.get_duration(y=y)

	# Calculate the amplitude envelope
	amplitude_envelope = librosa.feature.rms(y=y)[0]

	average_amplitude = round(np.mean(amplitude_envelope), 2)
	max_amplitude = round(np.max(amplitude_envelope), 2)
	result['average_amplitude'] = average_amplitude
	result['max_amplitude'] = max_amplitude
	print(average_amplitude)

	energy_multiplicator = max_amplitude / average_amplitude
	start_times = []
	if find_times:
		while True:
			# Set a threshold for detecting increasing energy
			threshold = round(average_amplitude * energy_multiplicator, 2)  # Adjust this value based on your analysis
			result['threshold'] = threshold
			# Find indices where the amplitude exceeds the threshold
			increasing_energy_indices = np.where(amplitude_envelope > threshold)[0]
			# time when amplitude > threshold
			time_chorus = librosa.times_like(amplitude_envelope)[increasing_energy_indices]

			start_times = []
			for index in range(len(time_chorus) - 1):
				if time_chorus[index] + 1 < time_chorus[index + 1]:
					if (len(start_times) == 0 or time_chorus[index + 1] > start_times[-1] + 10) \
							and time_chorus[index + 1] + 20 < full_duration \
							and time_chorus[index + 1] > 30:
						start_times.append(round(time_chorus[index + 1], 2))

			if len(start_times) > 2:
				break
			energy_multiplicator -= 0.05

		result['start_times'] = start_times

		bpm, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
		result['bpm'] = round(bpm, 2)

		tacts = 14
		while tacts >= bpm / 10:
			tacts -= 2

		piece_duration = 60 / bpm * tacts

		end_times = []
		for start_time in start_times:
			end_times.append(round(start_time + piece_duration, 2))
		result['end_times'] = end_times

	if draw_chart:
		# Plot the amplitude envelope and highlight areas of increasing energy
		plt.figure(figsize=(12, 4))
		librosa.display.waveshow(y, alpha=0.5)
		plt.plot(librosa.times_like(amplitude_envelope), amplitude_envelope, label='Amplitude Envelope', color='r')
		plt.scatter(librosa.times_like(amplitude_envelope)[increasing_energy_indices], amplitude_envelope[increasing_energy_indices], color='g', label='Increasing Energy')
		plt.title('Energy Distribution with Increasing Energy Detection')
		plt.xlabel('Time (s)')
		plt.ylabel('Amplitude')
		plt.legend()
		plt.show()

	return result


# Analyses song and fills row in db.
def fill_song_info(song: Song):
	if song.clip_path:
		result = analyze_track(song.clip_path)
		song \
			.set_clip_start_sec(result['start_times']) \
			.set_clip_end_sec(result['end_times']) \
			.save()
		print(f'Analysing song {song.id} was finished')


def reanalyze_songs(min_id: int = 300):
	songs = SongRepository().get_by_greater_id(min_id)
	for song in songs:
		fill_song_info(song)


def reanalyze_song(song_id: int):
	song = SongRepository().get_song_by_id(song_id)
	fill_song_info(song)


if __name__ == '__main__':
	# path = 'D:\\Artyom\\Проекты\\Python\\tcc-render\\production\\tcc 2024-03-16.mp4'
	path = 'D:\\Artyom\\Проекты\\Python\\tcc-render\\video_parts\\tcc\\457\\3.1.mp4'
	# path = 'D:\\Artyom\\Проекты\\Top Club Chart\\клипы чарта\\regulars\\AVAION, BUNT. - Other Side (Official Video).mp4'

	# print(analyze_track(
	# 	audio_path=path,
	# 	draw_chart=False,
	# 	find_times=False,
	# ))
	# reanalyze_songs(316)
