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



