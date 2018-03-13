
# https://staff.fnwi.uva.nl/r.vandenboomgaard/SP20162017/Python/Audio/rta_signaldisplay.html

import sys
import wave
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


if len(sys.argv) == 1:
    fname = "noise.wav"
else:
    fname = sys.argv[1]


wf = wave.open(fname, 'rb')
nchannels = wf.getnchannels() # 1: mono, 2: stereo
nbytesframe = wf.getsampwidth() # 1: unsigned byte, 2: signed int
framerate = wf.getframerate() # no of samples per second

if nbytesframe == 1:
       tp = np.uint8
else:
       tp = np.int16

N = framerate
x = np.fromstring(wf.readframes(N), tp)

if nchannels == 1:
       xleft = x
       xright = x
else:
       xleft = x[::2]
       xright = x[1::2]

# slices x[startAt:endBefore:skip]
# x[::2] means start beginning, end, skip by 2
# x[1::2] means start from 1, end, skip by 2

# >>> import numpy as np
# >>> na = np.arange(1,10)
# >>> na
# array([1, 2, 3, 4, 5, 6, 7, 8, 9])
# >>> ev = na[::2]  <== starts from beginning, to end, skip by 2
# >>> ev
# array([1, 3, 5, 7, 9])
# >>> od = na[1::2] <== starts from index 1, to end, skip by 2
# >>> od
# array([2, 4, 6, 8])
# >>>


# scale to -1.0 -- 1.0
nb_bits = 16
max_nb_bit = float(2**(nb_bits-1))  
samples = xleft / (max_nb_bit + 1.0) 

c = np.fft.fft(xleft)

plt.plot(c, 'r')
plt.show()

