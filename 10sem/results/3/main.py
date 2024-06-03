import numpy as np
import librosa.display

def findFrequencies(filename, output_path):
    y, sr = librosa.load(filename, sr=None, mono=True)

    D = np.abs(librosa.stft(y, window='hann'))

    frequencies = librosa.fft_frequencies(sr=sr)
    amplitudes = np.max(D, axis=1)

    min_frequency_index = np.argmax(amplitudes > np.max(amplitudes) * 0.01)  # Порог для исключения шума
    min_frequency = frequencies[min_frequency_index]

    max_frequency_index = len(frequencies) - np.argmax(amplitudes[::-1] > np.max(amplitudes) * 0.01) - 1
    max_frequency = frequencies[max_frequency_index]

    with open(output_path, 'w') as f:
        f.write(f'Minimum frequency: {min_frequency} Hz\n')
        f.write(f'Maximum frequency: {max_frequency} Hz\n')

findFrequencies('../1/А.wav', 'output/frequencies_А.txt')
findFrequencies('../1/И.wav', 'output/frequencies_И.txt')
findFrequencies('../1/kitten.wav', 'output/frequencies_kitten.txt')