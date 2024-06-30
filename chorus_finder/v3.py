import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from chorus_finder.base_version import BaseVersion

matplotlib.use('TkAgg')


class ChorusFinderV3(BaseVersion):
	def find_chorus(self, audio_path: str, draw_chart: bool, find_times: bool):
		result = dict()

		y, sr = librosa.load(audio_path)
		self.y = y
		self.sr = sr
		self.full_duration = librosa.get_duration(y=self.y)

		# Calculate the amplitude envelope
		self.amplitude_envelope = librosa.feature.rms(y=self.y)[0]

		average_amplitude = round(np.mean(self.amplitude_envelope), 2)
		max_amplitude = round(np.max(self.amplitude_envelope), 2)
		result['average_amplitude'] = average_amplitude
		result['max_amplitude'] = max_amplitude
		piece_duration = self.get_piece_duration()

		energy_multiplicator = max_amplitude / average_amplitude
		increasing_energy_indices = []
		start_times = []


		result = {
			'start_times': start_times
		}
		end_times = []
		for start_time in start_times:
			end_times.append(round(start_time + piece_duration, 2))
		result['end_times'] = end_times

		if draw_chart:
			self.show_plot(increasing_energy_indices)

		return result
