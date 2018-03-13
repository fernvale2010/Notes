
# http://blog.acipo.com/wave-generation-in-python/


import wave, struct, math

sampleRate = 44100.0 # hertz
duration = 1.0       # seconds

# Use different frequencies for the left and right channels
rFreq = 1760.00  # A
lFreq =  523.25  # C

wavef = wave.open('sound.wav','w')
wavef.setnchannels(2) # stereo
wavef.setsampwidth(2) 
wavef.setframerate(sampleRate)

for i in range(int(duration * sampleRate)):
    l = int(32767.0*math.cos(lFreq*math.pi*float(i)/float(sampleRate)))
    r = int(32767.0*math.cos(rFreq*math.pi*float(i)/float(sampleRate)))
    wavef.writeframesraw( struct.pack('<hh', l, r ) )

wavef.writeframes(b'0')
wavef.close()



# Interesting stuff
# http://blog.telenor.io/2015/10/26/machine-learning.html
# https://github.com/la3lma/movement-analysis/tree/master/data-gathering

