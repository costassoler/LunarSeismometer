import numpy as np
import scipy.signal as sg
from matplotlib import pyplot as plt

# load file 
data = np.load('FilterRecording2020_5_15_20_54.npz')['signals'] # get the signals outta there!

# impulse response occurs between 4300 and 4500
fftChunk = data[4300:4500]

fftChunk = sg.detrend(fftChunk) # detrend removes the mean + any linear trend over the interval (makes the endpoints 0)
# asssume the signal ~0 at the endpoints, no need to window

# I use rfft bc the signal is real. Normally when you take an fft of N time domain sample you get N samples back in the
# frequency domain, however half of the samples will be negative frequencies (dont think about it too hard) and half 
# positive. The points in the frequency domain will be equally spread out between -Fs/2 and Fs/2 (Fs=sampling frequency)
# (this is also where the nyquist limit comes from :) ) When the signal is purely real, the negative and positive frequencies
# are symetric, so you only need to calculate half

freqDomain = np.abs(np.fft.rfft(fftChunk)) # take the absolute value, fft returns complex values but we want the real magnitude

# With only the real half of the frequencies, we have N // 2 + 1 points spread out between 0 and Fs/2
# original signal is 200 points, so the fft will have 100 + 1 points

Fs = 40 # 40 hz sampling frequency

frequencies = np.arange(101) * Fs / (2 * 100) # scales the range 0-100 to 0 to Fs/2

# plot frequency and time domains

time = np.arange(200) / Fs # time in seconds of our chunk

f, (ax1, ax2) = plt.subplots(2,1)
ax1.plot(time,fftChunk)           # 0 centered time domain signal
ax2.plot(frequencies, freqDomain) # frequency domain view of the same signal
plt.show()

