import matplotlib.pyplot as plt
import librosa, base64
import librosa.display
import numpy as np
import os
from io import BytesIO
from PIL import Image 

class NosieLevelAlgorithm():
    def __str__(self):
        """Returns a string representation of the class."""

    # def get_graph():
    #     buffer = BytesIO()
    #     plt.savefig(buffer, format='png')
    #     buffer.seek(0)
    #     image_png = buffer.getvalue()
    #     graph = base64.b64encode(image_png)
    #     graph = graph.decode('utf-8')
    #     buffer.close()
    #     return graph

    def get_duration_librosa(file_path):
        audio_data, sample_rate = librosa.load(file_path)
        duration = librosa.get_duration(y=audio_data, sr=sample_rate)
        return duration

    def calculate_noise_density(audio_path, window_size=2048, hop_size=1024):
        # Load the audio file
        y, sr = librosa.load(audio_path)

        #compute the short-time Fourier transform (STFT)
        D = np.abs(librosa.stft(y, n_fft=window_size, hop_length=hop_size))**4

        #Density in decibels
        S = librosa.power_to_db(D, ref=np.max)

        #Estimate the noise Level in decibels
        noise_density = np.mean(S)

        return np.abs(noise_density)
    
    def plot_frequency_spectrum(self, file_path):
        array, sampling_rate = librosa.load(file_path)
        
        dft_input = array[:]

        #calculate the dft
        window = np.hanning(len(dft_input))
        windowed_input = dft_input * window
        dft = np.fft.rfft(windowed_input)

        #get the amplitude spectrum in decibels
        amplitude = np.abs(dft)
        amplitude_db = librosa.amplitude_to_db(amplitude, ref=np.max)

        #get the frequency bins
        frequency = librosa.fft_frequencies(sr=sampling_rate, n_fft=len(dft_input))

        plt.switch_backend('SVG')
        fig = plt.figure(figsize=(12, 4))
        plt.plot(frequency, amplitude_db)
        plt.xlabel("Frequency (Hz)")

        plt.ylabel("Amplitude (db)")
        plt.xscale("log")

        fig.savefig(f"media/graph_files/{os.path.basename(file_path)}.png", bbox_inches='tight', dpi=150)
        plt.show()
        plt.close(fig)
        return f"graph_files/{os.path.basename(file_path)}.png"

    def plot_wave_form(self, file_path):
        array, sampling_rate = librosa.load(file_path)
        fig = plt.figure(figsize=(12, 4))
        librosa.display.waveshow(array, sr=sampling_rate)

        fig.savefig(f"media/graph_files/{os.path.basename(file_path)}.png", bbox_inches='tight', dpi=150)
        plt.close(fig)
        return f"graph_files/{os.path.basename(file_path)}.png"

    def plot_spectogram(self, file_path):
        array, sampling_rate = librosa.load(file_path)
        D = librosa.stft(array)
        S_db = librosa.amplitude_to_db(np.abs(D))

        fig = plt.figure(figsize=(12, 4))
        librosa.display.specshow(S_db, x_axis="time", y_axis="hz")
        plt.colorbar()

        fig.savefig(f"media/graph_files/{os.path.basename(file_path)}.png", bbox_inches='tight', dpi=150)
        plt.close(fig)
        return f"graph_files/{os.path.basename(file_path)}.png"

    def plot_mel_spectogram(self, file_path):
        array, sampling_rate = librosa.load(file_path)
        S = librosa.feature.melspectrogram(y=array, sr=sampling_rate, n_mels=128, fmax=8000)
        S_db = librosa.power_to_db(S, ref=np.max)

        fig = plt.figure(figsize=(12, 4))
        librosa.display.specshow(S_db, x_axis="time", y_axis="mel", sr=sampling_rate, fmax=8000)
        plt.colorbar()

        fig.savefig(f"media/graph_files/{os.path.basename(file_path)}.png", bbox_inches='tight', dpi=150)
        plt.close(fig)
        return f"graph_files/{os.path.basename(file_path)}.png"

