import librosa
import librosa.display
import matplotlib
import numpy as np
from chorus_finder.base_version import BaseVersion

matplotlib.use('TkAgg')


class ChorusFinderV2(BaseVersion):
	def find_chorus(self, audio_path: str, draw_chart: bool, find_times: bool):
		result = dict()

		y, sr = librosa.load(audio_path)
		self.y = y
		full_duration = librosa.get_duration(y=y)

		# Calculate the amplitude envelope
		amplitude_envelope = librosa.feature.rms(y=y)[0]

		average_amplitude = round(np.mean(amplitude_envelope), 2)
		max_amplitude = round(np.max(amplitude_envelope), 2)
		result['average_amplitude'] = average_amplitude
		result['max_amplitude'] = max_amplitude
		print(average_amplitude)

		energy_multiplicator = max_amplitude / average_amplitude
		increasing_energy_indices = []
		if find_times:
			while True:
				# Set a threshold for detecting increasing energy
				threshold = round(average_amplitude * energy_multiplicator * 0.8, 2)  # Adjust this value based on your analysis
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
							# Distance 10 secs from previous chorus, 20 secs from song end and 30 secs from start
							start_times.append(round(time_chorus[index + 1], 2))

				if len(start_times) >= 1:
					break
				energy_multiplicator *= 0.8
				if energy_multiplicator < 1:
					print(f'Song {audio_path} has no start times {start_times}')
					break

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
			self.show_plot(increasing_energy_indices)

		return result
