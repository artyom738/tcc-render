import librosa
import librosa.display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('TkAgg')


def analyze_track(audio_path: str, draw_chart=False):
	# Load audio file
	# audio_path = 'test_results/!York - On The Beach (Kryder Remix).mp3'
	result = dict()
	y, sr = librosa.load(audio_path)

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

	bpm, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
	result['bpm'] = round(bpm, 2)

	tacts = 14
	while tacts >= bpm / 10:
		tacts -= 2

	piece_duration = 60 / bpm * tacts
	full_duration = librosa.get_duration(y=y)

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


if __name__ == '__main__':
	path = 'D:\\Artyom\\Проекты\\Python\\tcc-render\\test_results\\Aaron Smith - Dancin (Krono Remix).mp3'
	print(analyze_track(
		audio_path=path,
		draw_chart=False,
	))
