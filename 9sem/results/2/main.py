import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

filename = '../1/output/russkiy-narodnyiy-naigryish.wav'  # Замените на имя вашего файла
y, sr = librosa.load(filename, sr=None, mono=True)

# Построение спектрограммы с использованием оконного преобразования Фурье с окном Ханна
D = np.abs(librosa.stft(y, window='hann'))

# Преобразование амплитуд в децибелы
DB = librosa.amplitude_to_db(D, ref=np.max)

# Визуализация спектрограммы на логарифмической шкале
plt.figure(figsize=(10, 6))
librosa.display.specshow(DB, sr=sr, x_axis='time', y_axis='log', cmap='viridis')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram (Log scale)')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.savefig('output/spectrogram.png')
