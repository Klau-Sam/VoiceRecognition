from numpy import *
from scipy import *
import numpy as np
import scipy.io.wavfile
from scipy import signal as sig
import warnings
import glob

warnings.filterwarnings("ignore")


def funkcja(nazwa_pliku):
    # czytamy plik i wyciagamy czestotliwosc probkowania
    w, signal = scipy.io.wavfile.read(nazwa_pliku)
    # jesli sa dwa kanaly to je usredniamy

    if len(signal.shape) == 2:
        signal = [(s[0] + s[1]) / 2 for s in signal]

    signal = np.array(signal)
    n = len(signal)

    # Spektrum
    furier = abs(fft(signal))

    # Wyliczenie czestotliwosci i amplitud dla spektrum
    freqs = []
    signal1 = []
    for i in range(n):
        freq = i * w / n
        freqs.append(freq)

    signal1 = abs(furier) * 2 / len(signal)
    h = max(signal1)
    signal1 = signal1[signal1 != h]
    freqs = np.array(freqs)
    signal1 = np.array(signal1)

    # Sprawdzamy pierwsza polowe spektrum - lustrzane odbicie pomijamy
    freqs = freqs[:len(freqs) // 2]
    signal1 = signal1[:len(signal1) // 2]

    # metoda HARMONIC PRODUCT SPECTRUM
    signal1_HPS = signal1
    freqs_HPS = freqs
    final_length = 0
    min_downsample = 2
    max_downsample = 5

    for downsample_factor in reversed(range(2, 6)):
        downsampled = sig.decimate(signal1, downsample_factor)
        if downsample_factor == max_downsample:
            final_length = len(downsampled)  # ucinamy dlugosc aby byly takie same  a nastepnie
        signal1_HPS = signal1_HPS[:final_length] * downsampled[
                                                   :final_length]  # wymnażamy wartości widma razy jego przerzedzone wersje na odpowiadających sobie pozycjach
        freqs_HPS = freqs_HPS[:final_length]

    maximum = 0
    maxi = 0
    indeks = 0
    i = 0
    for freqency in signal1_HPS:
        i += 1
        if freqs[i] > 85:           # minimalna czestotliwosc podstawowa glosu to okolo 85 hz (u faceta)
            if freqency > maxi:
                maxi = freqency      # najwieksza wartosc iloczynu jest miejscem  gdzie znajduje się częstotliwość podstawowa.
                indeks = i
    # zakladamy ze mezczyzna ponizej 165 Hz
    if freqs[indeks] < 160:
        odp = "M"
    else:
        odp = "K"

    return odp


count = 0
correct = 0
files = glob.glob("train/*.wav")
for file in files:
    count += 1;
    gender = ((str(file[-5])))
    found = funkcja(file)
    if gender == found:
        correct += 1;

print(correct / count)
# funkcja("train/005_M.wav")
