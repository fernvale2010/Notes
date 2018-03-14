# https://stackoverflow.com/questions/24920346/filtering-a-wav-file-using-python

import numpy as np
import wave
import struct

freq = 440.0
data_size = 40000
fname = "High_A.wav"
frate = 11025.0  
amp = 64000.0    

sine_list_x = []
for x in range(data_size):
    sine_list_x.append(np.sin(2*np.pi*freq*(x/frate)))

wav_file = wave.open(fname, "w")

nchannels = 1
sampwidth = 2
framerate = int(frate)
nframes = data_size
comptype = "NONE"
compname = "not compressed"

wav_file.setparams((nchannels, sampwidth, framerate, nframes,
comptype, compname))

for s in sine_list_x:
    wav_file.writeframes(struct.pack('h', int(s*amp/2)))

wav_file.close()


# sine_signal = np.sin(2*np.pi*freq*(np.arange(data_size)/frate))
# wav_file.writeframes((sine_signal*amp/2).astype('h').tostring())


# http://matteolandi.blogspot.sg/2010/08/notes-about-fft-normalization.html
# samplerate = 44100
# N = 1024

# time = 1 / samplerate * np.arange(N)
# freq = samplerate / N * np.arange(N)
# f1 = 750
# a1 = 1.5
# f2 = 4400
# a2 = 4
# y = a1 * np.sin(2 * np.pi * f1 * time) + a2 * np.sin(2 * np.pi *f2 * time)
# h = np.fft.fft(y)
# pylab.plot(freq[:N // 2], np.abs(h[:N // 2]))
# pylab.show()

# # with normalization
# normalization = 2 / N
# h = np.fft.fft(y)
# pylab.plot(freq[:N // 2], normalization * np.abs(h[:N // 2]))
# pylab.show()
