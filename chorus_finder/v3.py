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
		increasing_energy_indices = []

		while True:
			# Set a threshold for detecting increasing energy
			threshold = round(average_amplitude * energy_multiplicator * 0.8, 2)
			result['threshold'] = threshold

			# Find indices where the amplitude exceeds the threshold
			increasing_energy_indices = np.where(amplitude_envelope > threshold)[0]

			# Time when amplitude > threshold
			time_chorus = librosa.frames_to_time(increasing_energy_indices, sr=sr)
			start_times = []

			for index in range(len(time_chorus) - 1):
				if time_chorus[index] + 1 < time_chorus[index + 1]:
					potential_start_time = time_chorus[index + 1]

					if (len(start_times) == 0 or potential_start_time > start_times[-1] + 10) \
						and potential_start_time + segment_duration < full_duration - 20 \
						and potential_start_time > 30:
						# Distance 10 secs from previous chorus, 20 secs from end and 30 secs from start

						# Calculate the average amplitude of the segment
						start_frame = librosa.time_to_frames(potential_start_time, sr=sr)
						end_frame = librosa.time_to_frames(potential_start_time + segment_duration, sr=sr)
						segment_amplitude = np.mean(amplitude_envelope[start_frame:end_frame])

						if segment_amplitude > threshold:
							start_times.append(round(potential_start_time, 2))

			if len(start_times) >= 3:
				break

			energy_multiplicator *= 0.9
			if energy_multiplicator < 1:
				print(f'Song {audio_path} has not enough start times {start_times}')
				break

		result['start_times'] = start_times

		if draw_chart:
			self.show_plot(increasing_energy_indices)

		return result
