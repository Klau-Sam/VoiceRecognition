from numpy import *
from scipy import *
import sys, getopt
import numpy as np
import scipy.io.wavfile
from scipy import signal as sig
import glob




def main(argv):
    # czytamy plik i wyciagamy czestotliwosc probkowania
    w, signal = scipy.io.wavfile.read(argv)
    # jesli sa dwa kanaly to je usredniamy

    if len(signal.shape) == 2:
        signal = [(s[0] + s[1]) / 2 for s in signal]

    signal = np.array(signal)
    n = len(signal)

    # Spektrum
    spectrum = abs(fft(signal))

    # Wyliczenie czestotliwosci i amplitud dla spektrum
    freqs = []
    signal1 = []
    for i in range(n):
        freq = i * w / n
        freqs.append(freq)

    signal1 = abs(spectrum) * 2 / len(signal)
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
        signal1_HPS = signal1_HPS[:final_length] * downsampled[:final_length]  # wymnażamy wartości widma razy jego przerzedzone wersje na odpowiadających sobie pozycjach
        freqs_HPS = freqs_HPS[:final_length]


    maxi = 0
    indeks = 0
    i = 0
    for freqency in signal1_HPS:
        i += 1
        if freqs[i] > 85:           # minimalna czestotliwosc podstawowa glosu to okolo 85 hz (u faceta)
            if freqency > maxi:
                maxi = freqency      # najwieksza wartosc iloczynu jest miejscem  gdzie znajduje się częstotliwość podstawowa.
                indeks = i
    # zakladamy ze mezczyzna ponizej 160 Hz
    if freqs[indeks] < 160:
        odp = "M"
    else:
        odp = "K"

    return odp



# Część sprawdzające % skuteczności na całej bazie nagrań:
# count = 0
# correct = 0
# itsnotman=0
# itsnotwoman=0
# files = glob.glob("train/*.wav")
# for file in files:
#     count += 1
#     gender = str(file[-5])
#     result = check_gender(file)
#     if gender=="K" and result == "M" : itsnotman+=1
#     if gender == "M" and result == "K": itsnotwoman += 1
#
#     if gender == result:
#         correct += 1
#
# print("skutecznosc wykrywania płci dla podanego zbioru nagrań to:")
# print(correct / count)
# print("ilość błędów: kobieta:",itsnotman,"mezczyzna:",itsnotwoman)





 #"aby sprawdzic wynik konkretnego nagrania podaj nazwe pliku jako argument(musi sie znajdowac w folderze train/"
if __name__ == "__main__":
   print(main(sys.argv[1]))
