import librosa
import librosa.display
import matplotlib.pyplot as plt


class BaseVersion:
	def __init__(self):
		self.y = None
		self.sr = None
		self.full_duration = None
		self.amplitude_envelope = None

	def get_piece_duration(self):
		bpm, beat_frames = librosa.beat.beat_track(y=self.y, sr=self.sr)

		tacts = 14
		while tacts >= bpm / 10:
			tacts -= 2

		# приводим bpm к float, чтобы не было numpy.ndarray
		bpm = float(bpm)

		piece_duration = 60 / bpm * tacts

		return round(piece_duration, 2)

	def show_plot(self, increasing_energy_indices):
		# Plot the amplitude envelope and highlight areas of increasing energy
		plt.figure(figsize=(12, 4))
		librosa.display.waveshow(self.y, alpha=0.5)
		amplitude_envelope = librosa.feature.rms(y=self.y)[0]
		plt.plot(librosa.times_like(amplitude_envelope), amplitude_envelope, label='Amplitude Envelope', color='r')
		plt.scatter(librosa.times_like(amplitude_envelope)[increasing_energy_indices],
		            amplitude_envelope[increasing_energy_indices], color='g', label='Increasing Energy')
		plt.title('Energy Distribution with Increasing Energy Detection')
		plt.xlabel('Time (s)')
		plt.ylabel('Amplitude')
		plt.legend()
		plt.show()
