import sys
import binascii
import getopt

inputfile = ''
outputfile = ''
conv = ''

usage = '{} -i <inputfile> -o <outputfile> -c <hex|bin>'

def parseArg(argv):
  global inputfile, outputfile, conv
  try:
    opts, args = getopt.getopt(argv,"hi:o:c:",["ifile=","ofile=","choice="])
  except getopt.GetoptError:
    print(usage.format(sys.argv[0]))
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print(usage.format(sys.argv[0]))
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg
    elif opt in ("-c", "--choice"):
      conv = arg

  if not inputfile and not outputfile and not conv:
    print(usage.format(sys.argv[0]))
    sys.exit(2)



def toHex():
  global inputfile, outputfile, conv
  with open(inputfile, 'rb') as f:
    content = f.read()

  # convert to hex
  #------------------
  hexStr = str(binascii.hexlify(content), 'ascii')

  # split into rows with 8 pairs of hexcode each..
  hexby8 = '\n'.join(hexStr[i:i+16] for i in range(0, len(hexStr), 16))

  # create a list of elements with 8 pairs of hexcode..
  formatted_by8 = list(hexby8.split())
  #print(formatted_by8)

  a = [] # empty array

  # add '0x' to each hexcode..
  for elem in formatted_by8:
    if False: # set to True if we want to add '0x'
      a.append('0x' + ', 0x'.join(elem[i:i+2] for i in range(0, len(elem), 2)))
    else:
      a.append(' '.join(elem[i:i+2] for i in range(0, len(elem), 2)))

  with open(outputfile, 'w') as of:
    for i in a:
      #print(i)
      of.write(i + '\n')


def toBin():
  global inputfile, outputfile, conv
  # now convert back to binary
  #---------------------------
  with open(inputfile, 'r') as f:
    content = f.read()

  hexStr = bytes(''.join(content.split()), "utf-8")
  binStr = binascii.unhexlify(hexStr)

  with open(outputfile, 'wb') as f:
    f.write(binStr)



def main(argv):
  global inputfile, outputfile, conv

  print('Hello\r\n')

  parseArg(argv)
  if conv == 'hex':
    toHex()
  elif conv == 'bin':
    toBin()

  sys.exit (1)

if __name__ == "__main__":
   main(sys.argv[1:])

