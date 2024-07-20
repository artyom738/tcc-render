import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from chorus_finder.base_version import BaseVersion

matplotlib.use('TkAgg')


class ChorusFinderV3(BaseVersion):
	def find_chorus(self, audio_path: str, draw_chart: bool, find_times: bool):
		y, sr = librosa.load(audio_path)
		self.y = y
		self.sr = sr
		full_duration = librosa.get_duration(y=y)

		# Calculate the amplitude envelope
		amplitude_envelope = librosa.feature.rms(y=y)[0]
		average_amplitude = round(np.mean(amplitude_envelope), 2)
		max_amplitude = round(np.max(amplitude_envelope), 2)
		segment_duration = self.get_piece_duration()

		result = {
			'average_amplitude': average_amplitude,
			'max_amplitude': max_amplitude
		}

		print(average_amplitude)
		energy_multiplicator = max_amplitude / average_amplitude
		increasing_times = []
		start_times = []

		while True:
			# Set a threshold for detecting increasing energy
			threshold = round(average_amplitude * energy_multiplicator, 2)
			result['threshold'] = threshold

			# Find indices where the amplitude exceeds the threshold
			increasing_energy_indices = np.where(amplitude_envelope > threshold)[0]

			# Time when amplitude > threshold
			time_chorus = librosa.frames_to_time(increasing_energy_indices, sr=sr)

			for index in range(len(time_chorus) - 1):
				if time_chorus[index] + 1 < time_chorus[index + 1]:
					potential_start_time = time_chorus[index + 1]

					if (len(increasing_times) == 0 or potential_start_time > increasing_times[-1] + 10) \
						and potential_start_time + segment_duration < full_duration - 10 \
						and potential_start_time > 30:
						# Distance 10 secs from previous chorus, 20 secs from end and 30 secs from start
						increasing_times.append(round(potential_start_time, 2))

			if len(increasing_times) > 5:
				break
			if energy_multiplicator > 1:
				energy_multiplicator *= 0.8
			else:
				break

		segment_amplitudes = {}
		for increasing_time in increasing_times:
			# Calculate the average amplitude of the segment
			start_frame = librosa.time_to_frames(increasing_time, sr=sr)
			end_frame = librosa.time_to_frames(increasing_time + segment_duration, sr=sr)
			segment_amplitude = np.mean(amplitude_envelope[start_frame:end_frame])
			if segment_amplitude > average_amplitude:
				segment_amplitudes[increasing_time] = segment_amplitude

		sorted_segment_amplitudes = sorted(segment_amplitudes.items(), key=lambda x: x[1], reverse=True)
		for i in range(3 if len(segment_amplitudes) >= 3 else len(segment_amplitudes)):
			start_times.append(round(sorted_segment_amplitudes[i][0], 2))

		start_times.sort()
		result['start_times'] = start_times
		result['end_times'] = [round(start_time + segment_duration, 2) for start_time in start_times]

		# self.show_plot(increasing_energy_indices)
		if draw_chart:
			self.show_plot(increasing_energy_indices)

		return result
