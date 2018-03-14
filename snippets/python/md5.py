

from hashlib import md5
import numpy as np
import wave, struct
import hashlib


def digest(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


wf = wave.open('sine.wav', 'rb')
data = np.fromstring(wf.readframes(800), np.int16)
da1 = data.tobytes()
hash = md5(da1)
print(hash.hexdigest())


message = b'hello'
da2 = np.asarray(message)
print(md5(da2).hexdigest())

print(digest(message))


