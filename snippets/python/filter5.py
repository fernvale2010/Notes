import collections as coll
import csv
import matplotlib.pyplot as plt
import numpy as np
import sys


fs = 100.0
dt = 1.0/fs
alpha = 0.02

Sample = coll.namedtuple("Sample",
    "accZ accY accX rotZ rotY rotX r acc_angZ acc_angY acc_angX cfZ cfY cfX")

def samples_from_file(fname):
    with open(fname) as f:
        next(f)  # discard header row
        csv_reader = csv.reader(f, dialect='excel')

        for i, row in enumerate(csv_reader, 1):
            try:
                values = [float(x) for x in row]
                yield Sample(*values)
            except Exception:
                lst = list(row)
                print("Bad line %d: len %d '%s'" % (i, len(lst), str(lst)))


samples = list(samples_from_file("data.csv"))

cfx = np.zeros(len(samples))

# Excel formula: =R12
cfx[0] = samples[0].acc_angX
# Excel formula: =0.98*(U12+N13*0.01)+0.02*R13
# Excel: U is cfX  N is rotX  R is acc_angX
for i, s in enumerate(samples[1:], 1):
    cfx[i] = (1.0 - alpha) * (cfx[i-1] + s.rotX*dt) + (alpha * s.acc_angX)

check_line = [s.cfX - cf for s, cf in zip(samples, cfx)]

plt.figure(1)
plt.plot(check_line)
plt.plot(cfx)
plt.show()

