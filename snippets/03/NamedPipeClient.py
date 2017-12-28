
# http://jonathonreinhart.blogspot.sg/2012/12/named-pipes-between-c-and-python.html
import time
import struct

f = open(r'\\.\pipe\NPtest', 'r+b', 0)
i = 1

while True:
    # s = 'Message[{0}]'.format(i)
    print("Enter a message: (quit) to quit")
    s = input()
    if s == 'quit':
        break

    i += 1

    print(type(s))
        
    f.write(struct.pack('I', len(s)))
    f.write(s.encode('utf-8'))   # Write str length and str
    f.seek(0)                               # EDIT: This is also necessary
    print('Wrote:', s)

    n = f.read(4)    # Read str length
    s = f.read(n[0])                           # Read str
    f.seek(0)                               # Important!!!
    print('Read:', s.decode('utf-8'))

    # time.sleep(2)

# This works also..
# while True:
#     s = 'Message[{0}]'.format(i)
#     i += 1
        
#     f.write(struct.pack('I', len(s)))
#     f.write(s.encode('utf-8'))
#     f.seek(0)
#     print('Wrote:', s)

#     x = f.read(4)
#     s = f.read(x[0])
#     f.seek(0)
    
#     print('Read:', s.decode('utf-8'))
#     time.sleep(2)
