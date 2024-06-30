import librosa
import librosa.display
import matplotlib
import numpy as np
from chorus_finder.base_version import BaseVersion

matplotlib.use('TkAgg')


class ChorusFinderV1(BaseVersion):
	def find_chorus(self, audio_path: str, draw_chart: bool, find_times: bool):
		# Load audio file
		# audio_path = 'test_results/!York - On The Beach (Kryder Remix).mp3'
		result = dict()
		y, sr = librosa.load(audio_path)
		self.y = y

		# Calculate the amplitude envelope
		amplitude_envelope = librosa.feature.rms(y=y)[0]

		average_amplitude = round(np.mean(amplitude_envelope), 2)
		result['average_amplitude'] = average_amplitude
		# Set a threshold for detecting increasing energy
		threshold = round(average_amplitude * 1.7, 2)  # Adjust this value based on your analysis

		result['threshold'] = threshold

		# Find indices where the amplitude exceeds the threshold
		increasing_energy_indices = np.where(amplitude_envelope > threshold)[0]

		# time when amplitude > threshold
		time_chorus = librosa.times_like(amplitude_envelope)[increasing_energy_indices]

		tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
		if tempo < 100:
			tempo = tempo * 2
		result['bpm'] = round(tempo, 2)

		full_duration = librosa.get_duration(y=y)
		piece_duration = 600 / tempo

		start_times = []
		for index in range(len(time_chorus) - 1):
			if time_chorus[index] + 1 < time_chorus[index + 1]:
				if (len(start_times) == 0 or time_chorus[index + 1] > start_times[-1] + 10) \
						and time_chorus[index + 1] + 20 < full_duration \
						and time_chorus[index + 1] > 30:
					start_times.append(round(time_chorus[index + 1], 2))

		result['start_times'] = start_times

		end_times = []
		for start_time in start_times:
			end_times.append(round(start_time + piece_duration, 2))
		result['end_times'] = end_times

		if draw_chart:
			self.show_plot(increasing_energy_indices)

		return result
