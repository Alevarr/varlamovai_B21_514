import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
from scipy.signal import savgol_filter

filename = '../1/output/russkiy-narodnyiy-naigryish.wav'
y, sr = librosa.load(filename, sr=None, mono=True)

D = np.abs(librosa.stft(y, window='hann'))
DB = librosa.amplitude_to_db(D, ref=np.max)

noise_level = np.mean(DB)

# Применение фильтра Савицкого-Голея для удаления шума
y_denoised = savgol_filter(y, window_length=101, polyorder=3)

# Построение спектрограммы очищенного сигнала
D_denoised = np.abs(librosa.stft(y_denoised, window='hann'))
DB_denoised = librosa.amplitude_to_db(D_denoised, ref=np.max)

# Визуализация исходной спектрограммы
plt.figure(figsize=(12, 8))

plt.subplot(2, 1, 1)
librosa.display.specshow(DB, sr=sr, x_axis='time', y_axis='log', cmap='viridis')
plt.colorbar(format='%+2.0f dB')
plt.title('Original Spectrogram (Log scale)')

# Визуализация спектрограммы очищенного сигнала
plt.subplot(2, 1, 2)
librosa.display.specshow(DB_denoised, sr=sr, x_axis='time', y_axis='log', cmap='viridis')
plt.colorbar(format='%+2.0f dB')
plt.title('Denoised Spectrogram (Log scale)')

plt.tight_layout()
plt.savefig('output/comparison_spectrogram.png')

sf.write('output/denoised_audio.wav', y_denoised, sr)
