import numpy as np
import matplotlib.pyplot as plt
import librosa.display

def harmonics(filename, output_path_spect, output_path_txt):
    y, sr = librosa.load(filename, sr=None, mono=True)

    # Построение спектрограммы с использованием оконного преобразования Фурье с окном Ханна
    D = np.abs(librosa.stft(y, window='hann'))
    DB = librosa.amplitude_to_db(D, ref=np.max)

    # Вычисление амплитуд для каждой частоты
    amplitudes = np.mean(D, axis=1)

    # Поиск обертонов
    harmonics_count = np.zeros(D.shape[0])
    frequencies = librosa.fft_frequencies(sr=sr)

    for i, freq in enumerate(frequencies):
        if freq == 0:
            continue
        harmonic_freqs = np.arange(freq, sr / 2, freq)
        harmonic_indices = np.searchsorted(frequencies, harmonic_freqs)
        harmonics_count[i] = np.sum(amplitudes[harmonic_indices])

    # Найти частоту с наибольшим количеством обертонов
    max_harmonics_index = np.argmax(harmonics_count)
    max_harmonics_frequency = frequencies[max_harmonics_index]

    plt.figure(figsize=(10, 6))
    librosa.display.specshow(DB, sr=sr, x_axis='time', y_axis='log', cmap='viridis')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram (Log scale)')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    plt.axhline(y=max_harmonics_frequency, color='r', linestyle='--',
                label=f'Max harmonics: {max_harmonics_frequency} Hz')
    plt.legend()

    plt.savefig(output_path_spect)

    with open(output_path_txt, 'w') as f:
        f.write(f'Frequency with most harmonics: {max_harmonics_frequency} Hz\n')

    print(f'Frequency with most harmonics: {max_harmonics_frequency} Hz')

harmonics('../1/А.wav', 'output/А_harmonics_frequency_spect.png', 'output/А_harmonics_frequency.txt')
harmonics('../1/И.wav', 'output/И_harmonics_frequency_spect.png', 'output/И_harmonics_frequency.txt')
harmonics('../1/kitten.wav', 'output/kitten_harmonics_frequency_spect.png', 'output/kitten_harmonics_frequency.txt')