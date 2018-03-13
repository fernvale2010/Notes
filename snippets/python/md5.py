

from hashlib import md5
import numpy as np
import wave, struct


wf = wave.open('sine.wav', 'rb')
data = np.fromstring(wf.readframes(800), np.int16)
da1 = data.tobytes()
hash = md5(da1)
print(hash.hexdigest())

