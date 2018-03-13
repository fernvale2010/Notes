# https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files

import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import wave, numpy as np
import heapq
import argparse

# fs, data = wavfile.read('noise.wav') # load the data
# a = data.T[0] # this is a two channel soundtrack, I get the first track
# b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
# c = fft(b) # calculate fourier transform (complex numbers list)
# d = len(c)/2  # you only need half of the fft list (real signal symmetry)

# k = arange(len(data))
# T = len(data)/fs  # where fs is the sampling frequency
# frqLabel = k/T 

# plt.plot(abs(c[:(d-1)]), frqLabel, 'r') 
# plt.show()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="input filename")
args = vars(ap.parse_args())


fname = args['input'] # input('Enter file: ')
print(fname)

try:
    wf = wave.open(fname, 'r')
    pass
except Exception as e:
    print("Cannot open file")
    print(e)
    exit()
else:
    pass
finally:
    pass


#nchannels=1, sampwidth=2, framerate=800, nframes

nchannels = wf.getnchannels()
sampwidth = wf.getsampwidth()
framerate = wf.getframerate()
nframes = wf.getnframes()

if sampwidth == 1:
    tp = np.int8
else:
    tp = np.int16

data = np.fromstring(wf.readframes(nframes),tp)

if nchannels == 1:
       xleft = data
       xright = data
else:
       xleft = data[::2]
       xright = data[1::2]


nb_bits = 16
max_nb_bit = float(2**(nb_bits-1))  
samples = xleft / (max_nb_bit + 1.0) 


# b=[(ele/2**16.)*2-1 for ele in data] # 2 bytes (16 bit) per sample normalize to (-1,1)
b = samples
c = fft(b)
d = len(c)//2

k = np.arange(d)
T = len(k)/framerate  # where fs is the sampling frequency
frqLabel = k/T 


fftfreq = np.fft.fftfreq(nframes, 1/framerate)


hi = max(abs(c[1:d]))
print(hi)
print("bin 0 = ", abs(c[0]))

highest = (heapq.nlargest(2, abs(c[1:d])))
print(highest)

idx = []
for i in range(0, len(highest)):
    idx.append(np.where(abs(c[1:d]) == highest[i])[0])
    print(highest[i], idx[i])

dtmf_dict = {
'0': [941, 1336],
'1': [697, 1209],
'2': [697, 1336],
'3': [697, 1477],
'4': [770, 1209],
'5': [770, 1336],
'6': [770, 1477],
'7': [852, 1209],
'8': [852, 1336],
'9': [852, 1477],
}


print("\r\n")
freq1 = fftfreq[idx[0] + 1][0]
freq2 = fftfreq[idx[1] + 1][0]
print(abs(c[idx[0] + 1]), "freq = ", freq1) # need to +1 for c[] since the max search is on c[1:]
print(abs(c[idx[1] + 1]), "freq = ", freq2)


freq = [int(freq1), int(freq2)]
freq.sort()
for k in dtmf_dict.keys():
    f = dtmf_dict.get(k)
    f.sort() # redundant, already sorted..
    print("standard=", f, "computed=", freq)
    res = [abs(m - n) for m,n in zip(f,freq)]
    # print(res)
    # if res[0] < 10 and res[1] < 10:
    if all(x<10 for x in res):
        print("found - %s" % k)
        break


    




# print("\r\n")
# for i in range(140, 150, 1):
#     print(abs(c[i]), fftfreq[i])


# for i in range(250, 260, 1):
#     print(abs(c[i]), fftfreq[i])


# plt.plot(abs(c[:d]), 'r') 

# plt.plot(fftfreq[1:d], abs(c[1:d]), 'Grey')
# plt.show()



