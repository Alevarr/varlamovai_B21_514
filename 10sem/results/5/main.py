import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

def find_formants(filename, output_file):
    y, sr = librosa.load(filename, sr=None, mono=True)

    D = np.abs(librosa.stft(y, window='hann'))
    DB = librosa.amplitude_to_db(D, ref=np.max)

    # Найти три самые сильные форманты
    frame_length = int(0.1 * sr)  # Длина фрейма в выборках (0.1 секунды)
    hop_length = frame_length // 2  # Половина длины фрейма для перекрытия

    formants = []

    for t in range(0, len(y), hop_length):
        frame = y[t:t + frame_length]
        if len(frame) < frame_length:
            break

        D_frame = np.abs(librosa.stft(frame, window='hann'))
        frequencies = librosa.fft_frequencies(sr=sr)
        amplitudes = np.mean(D_frame, axis=1)

        # Найти три самые сильные частоты в окрестности Δf = 40-50 Гц
        peaks = np.argsort(amplitudes)[-3:]  # Индексы трех самых сильных частот
        formants.extend(frequencies[peaks])

    # Сгруппировать и найти средние значения формант
    formants = np.array(formants)
    formant1 = formants[::3]
    formant2 = formants[1::3]
    formant3 = formants[2::3]

    formant1_mean = np.mean(formant1)
    formant2_mean = np.mean(formant2)
    formant3_mean = np.mean(formant3)

    with open(output_file, 'w') as f:
        f.write(f'Formant 1: {formant1_mean} Hz\n')
        f.write(f'Formant 2: {formant2_mean} Hz\n')
        f.write(f'Formant 3: {formant3_mean} Hz\n')

find_formants('../1/А.wav', 'output/А_formants.txt')
find_formants('../1/И.wav', 'output/И_formants.txt')
find_formants('../1/kitten.wav', 'output/kitten_formants.txt')

