import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

filename = '../1/output/russkiy-narodnyiy-naigryish.wav'  # Указанный вами путь к файлу
y, sr = librosa.load(filename, sr=None, mono=True)

D = np.abs(librosa.stft(y, window='hann'))
DB = librosa.amplitude_to_db(D, ref=np.max)

window_length_t = int(0.1 * sr / 2)  # Окно по времени (в выборках)
window_length_f = 40  # Окно по частоте (в индексах спектрограммы)

# Вычисление энергии
energy = np.sum(D**2, axis=0)

# Моменты времени с наибольшей энергией
max_energy_indices = np.argpartition(energy, -10)[-10:]  # Индексы 10 наибольших энергий
max_energy_times = librosa.frames_to_time(max_energy_indices, sr=sr)

plt.figure(figsize=(10, 6))
librosa.display.specshow(DB, sr=sr, x_axis='time', y_axis='log', cmap='viridis')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram with high energy moments')
plt.xlabel('Time')
plt.ylabel('Frequency')

# Отметка моментов времени с наибольшей энергией
for t in max_energy_times:
    plt.axvline(x=t, color='r', linestyle='--')

plt.savefig('output/energy_moments.png')
