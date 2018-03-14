

import sys
import os
import argparse


def doFileOps(fname):
    x = b"The quick brown fox jumps over the lazy dog"
    print(len(x))
    f = r"{}".format(fname)
    print(f)
    size = os.stat(f).st_size
    fp = open(f, "rb+") # open file for update
    fp.seek(0)
    print(size)
    while size > 0:
        fp.write(x)
        size = size - len(x)
        #print(size)
    fp.close()



ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="input filename")
args = vars(ap.parse_args())

fname = args['input'] # input('Enter file: ')
print(fname)

try:
    doFileOps(fname)
except Exception as e:
    print("Cannot open file")
    print(e)
    exit()
else:
    pass
finally:
    pass

