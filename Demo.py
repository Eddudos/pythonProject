from scipy.io import wavfile # scipy library to read wav files
import numpy as np
# import sys

AudioName = "APN.wav" # Audio File
fs, Audiodata = wavfile.read(AudioName)
# np.set_printoptions(threshold=sys.maxsize)
Audiodata = Audiodata[0:, 0]
print(Audiodata)

for i in range(len(Audiodata)):
    if 460 > Audiodata[i] > -460:
        Audiodata[i] = 0

# Plot the audio signal in time
import matplotlib.pyplot as plt
plt.plot(Audiodata)
plt.title('Audio signal in time',size=16)

# Spectrum
from scipy.fftpack import fft # fourier transform
n = len(Audiodata)
AudioFreq = fft(Audiodata)
AudioFreq = AudioFreq[0:int(np.ceil((n+1)/2.0))] #Half of the spectrum
MagFreq = np.abs(AudioFreq) # Magnitude
MagFreq = MagFreq / float(n)

# power spectrum
MagFreq = MagFreq**2
if n % 2 > 0: # ffte odd
    MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
else: # fft even
    MagFreq[1:len(MagFreq) - 1] = MagFreq[1:len(MagFreq) - 1] * 2

plt.figure()
np.seterr(divide = 'ignore') # Get rid of RuntimeWarning divide by zero encountered in log10
freqAxis = np.arange(0, int(np.ceil((n+1)/2.0)), 1.0) * (fs / n)
plt.plot(freqAxis/1000.0, 10*np.log10(MagFreq))  # Power spectrum
plt.xlabel('Frequency (kHz)'); plt.ylabel('Power spectrum (dB)')

# Spectrogram
from scipy import signal
N = 512  # Number of points in the fft
f, t, Sxx = signal.spectrogram(Audiodata, fs, nfft=N)
plt.figure()
plt.pcolormesh(t, f,10*np.log10(Sxx), shading='auto') # dB spectrogram
# plt.pcolormesh(t, f,Sxx) # Lineal spectrogram
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [seg]')
plt.title('Spectrogram with scipy.signal',size=16)

plt.show()
