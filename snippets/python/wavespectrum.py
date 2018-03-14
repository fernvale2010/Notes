# https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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


def find_dtmf(f1, f2):
    freq = [int(f1), int(f2)]
    freq.sort()
    for k in dtmf_dict.keys():
        f = dtmf_dict.get(k)
        f.sort() # redundant, already sorted..
        print("standard=", f, "computed=", freq)
        res = [abs(m - n) for m,n in zip(f,freq)] # compute difference between measured and standard freq..
        # print(res)
        # if res[0] < 10 and res[1] < 10:
        if all(x<10 for x in res):  # computed difference < 10 => found the dtmf digit
            return k
    return "No match"


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
c = rfft(b) # use the real number form
d = len(c)//2

k = np.arange(d)
T = len(k)/framerate  # where fs is the sampling frequency
frqLabel = k/T 


fftfreq = np.fft.rfftfreq(nframes, 1/framerate) # use the real number form


hi = max(abs(c[1:d]))
print(hi)
print("bin 0 = ", abs(c[0]))

highest = (heapq.nlargest(2, abs(c[1:d]))) # find 2 largest elements from c[]
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

# print("DTMF - %s" % find_dtmf(freq1, freq2)) # uncomment to find dtmf digit

# print("\r\n")
# for i in range(140, 150, 1):
#     print(abs(c[i]), fftfreq[i])


# for i in range(250, 260, 1):
#     print(abs(c[i]), fftfreq[i])

ax = plt.axes()
# xmarks=[i for i in range(int(min(abs(fftfreq))), int(max(abs(fftfreq))/2),1000)]
# plt.xticks(xmarks)

ax.xaxis.set_major_locator(ticker.MultipleLocator(1000)) # big ticks
ax.xaxis.set_minor_locator(ticker.MultipleLocator(100))  # small ticks

plt.xlim(min(abs(fftfreq)), max(abs(fftfreq))//2)

# plt.plot(abs(c[:d]), 'Grey') 

# color: 
# 'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'
#

N = len(samples)
# N = nframes
normalization = 2 / N

# plt.plot(samples, 'C0') 
plt.plot(fftfreq[1:d], normalization * abs(c[1:d]), 'grey')
plt.show()



