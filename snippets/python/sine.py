import matplotlib.pyplot as plt
import numpy as np
import random
import wave, struct


Fs = 800
f = 50 # 50 hz
sample = 800
x = np.arange(sample)
noise = 0.0008*np.asarray(random.sample(range(0,1000),sample))
 
y = 32767.0 * (np.sin(2 * np.pi * f * x / Fs)+noise)
y1 = 32767.0 * (np.sin(2 * np.pi * f * x / Fs)) # clean signal

wavef = wave.open('noise.wav','w')
wavef.setnchannels(1) # stereo=2, mono=1
wavef.setsampwidth(2) 
wavef.setframerate(sample)

for i in range(int(1 * sample)):
    wavef.writeframesraw( struct.pack('<h', int(y[i])//2) )

# wavef.writeframes(b'\0')
wavef.writeframes(b'')
wavef.close()


wavef = wave.open('sine.wav','w')
wavef.setnchannels(1) # stereo=2, mono=1
wavef.setsampwidth(2) 
wavef.setframerate(sample)

for i in range(int(1 * sample)):
    wavef.writeframesraw( struct.pack('<h', int(y1[i])//2) )

# wavef.writeframes(b'\0')
wavef.writeframes(b'')
wavef.close()





# plt.plot(x, y)
# plt.xlabel('voltage(V)')
# plt.ylabel('sample(n)')
# plt.show()



# https://forums.ni.com/t5/LabVIEW/Adding-low-frequency-noise-to-a-sine-function/td-p/3728126
# Let's say our Signal of Interest (here called "Signal") is 5 sin (2 pi 1 t) (amplitude 5, frequency 1 Hz).  
# Consider the following Signal + Noise:

#    Signal + 1.2 sin (2 pi 5.36 t + 1.2) + 1.4 sin (2 pi 7.34 t + 0.3) + 0.9 sin (2 pi 9.24 t - 0.45).

# There are three other sinusoids mixed in, with low amplitude, frequencies between 5 and 10 Hz (so low frequency), 
# random phases (so they don't start "in sync"), and the frequencies are not multiples of each other (so the sum never repeats).  
# So the sum represents Signal + noise.  But what is "t"?  Time starts at 0, and increments by 0.01 each sample 
# (since you are sampling at 100 Hz).  


# numpy array print formatter: This only affects printout, but doesn't change the values..
# float_formatter = lambda x: "%.2f" % x
# np.set_printoptions(formatter={'float_kind':float_formatter})
# OR
# np.set_printoptions(formatter={'float_kind': lambda x: "%.2f" % x})

# to reset to defaults:
# np.set_printoptions() 
# np.set_printoptions(formatter=None)


# unpacking: https://stackoverflow.com/questions/23631579/struct-error-unpack-requires-a-string-argument-of-length-4-audio-file
#
# The format string provided to struct has to tell it exactly the format of the second argument. 
# For example, "there are one hundred and three unsigned shorts". The way you've written it, the format 
# string says "there is exactly one float". But then you provide it a string with way more data than that, and it barfs.
#
# So issue one is that you need to specify the exact number of packed c types in your byte string. 
# In this case, 512 (the number of frames) times the number of channels (likely 2, but your code doesn't take this into account).
#
# The second issue is that your .wav file simply doesn't contain floats. If it's 8-bit, it contains unsigned chars, 
# if it's 16 bit it contains signed shorts, etc. You can check the actual sample width for your .wav by doing fp.getsampwidth().
#
# So then: let's assume you have 512 frames of two-channel 16 bit audio; you would write the call to struct as something like:
#
# channels = fp.getnchannels()
# ...
#
# tempb = fp.readframes(512);
# tempb2 = struct.unpack('{}h'.format(512*channels), tempb)

# struct pack/unpack: formatting types
# <      - little-endian
# >      - big-endian
# !      - network order (big-endian)
# @, =   - native order
# b,B    - signed and unsigned char
# h,H    - signed short and unsigned short


# https://www.researchgate.net/post/Can_someone_provide_me_a_Python_program_to_calculate_fundamental_frequency_and_other_frequencies_of_an_unknown_signal_with_01_or_001_Hz_accuracy

# If you apply FFT to a number of samples taken in the time interval T then the output represents the 
# frequencies 0 f, 1 f, 2 f, ... with f = 1 / T.  If you need a resolution of 0.1 Hz you have to feed 
# into the FFT samples taken within 10 s;  a resolution of 0.01 s would be based on samples taken in 100 s. 
# If this are too much data to process in real time, the next question is:  What is the maximum frequency 
# you are interested in?  With 16 kHz sampling frequency your upper limit would be 8 kHz. (Nyquist)
# If your signal has a spectrum containing virtually only *one* frequency with minor noise (as on the power 
# lines, as long as there are no control signals added) then a much simpler algorithm would be (as used in 
# frequency counters if the frequency is low):
# Determine the time T between each second zero voltage crossing, and compute f = 1 / T.  By computing 
# the average value of several results you could eliminate noise.
# To determine the presence of other frequencies above the line frequency, you could first send your samples 
# through a (digital) high pass filter, and then decide if the amplitude is above a threshold value.
# But if you really need a spectrum, and your hardware is too slow, I'm afraid you have to use a Digital Signal Processor.
#
# Resolution of 0.1Hz => we want to "see" frequencies that varies by 0.1Hz, to do that, we need 10s of samples
#


# Wave files are unsigned for 8 bits samples, signed for 9 bits and above.


# The sampling frequency (Fs) has to be at least twice the highest frequency component in the signal (whether you 
# are interested in that specific frequency or not) otherwise you get aliasing (look it up). The number of bins then 
# determines the resolution of each bin (or vice versa - the required resolution determines the minimum number of bins). 
# For a number of bins N, the resolution of each bin is Fs/N.
# If you don't low pass filter the incoming signal to, say, below 100Hz, the number of bins required will be very high. 
# E.g. A sampling rate of 8000Hz will require a minimum of 8000 bins to get 1Hz resolution


# https://www.norwegiancreations.com/2017/08/what-is-fft-and-how-can-you-implement-it-on-an-arduino/
# Bins
# The term bins is related to the result of the FFT, where every element in the result array is a bin. One can say this 
# is the “resolution” of the FFT. Every bin represent a frequency interval, just like a histogram. The number of bins you 
# get is half the amount of samples spanning the frequency range from zero to half the sampling rate. (nyquist)


# https://stackoverflow.com/questions/7337709/why-do-i-need-to-apply-a-window-function-to-samples-when-building-a-power-spectr
# I have found for several times the following guidelines for getting the power spectrum of an audio signal:

# 1) collect N samples, where N is a power of 2

# 2) apply a suitable window function to the samples, e.g. Hanning

# 3) pass the windowed samples to an FFT routine - ideally you want a real-to-complex FFT but if all you have a 
#    is complex-to-complex FFT then pass 0 for all the imaginary input parts

# 4) calculate the squared magnitude of your FFT output bins (re * re + im * im)

# 5) (optional) calculate 10 * log10 of each magnitude squared output bin to get a magnitude value in dB

# Now that you have your power spectrum you just need to identify the peak(s), which should be pretty straightforward 
# if you have a reasonable S/N ratio. Note that frequency resolution improves with larger N. For the above example of 
# 44.1 kHz sample rate and N = 32768 the frequency resolution of each bin is 44100 / 32768 = 1.35 Hz.



