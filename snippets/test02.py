import binascii
import sys
import json

# [] for lists, () for tuples, {} for dictionaries
def toUpp(str):
	return str.upper()


print('{} {}'.format('one', 'two'))

tu = ('hello', 'this', 'is', 'a', 'good', 'story')
print(tu)
li = list(tu)
print(li)

uppTu = list(map(toUpp, tu))
print(uppTu)

# lambda expression: meaning - take each item in tu as x, and apply x.upper(), the map function returns an iterator
uppTu2 = list(map(lambda x: x.upper(), tu))
print(uppTu2)

print(json.dumps(uppTu2, sort_keys=True, indent=3, separators=(',', ': ')))


# byte literals with b"", as compared to string which is unicode
content = b"test1234TEST5678abcdefgh12345678"
hexStr = str(binascii.hexlify(content), 'ascii')


# list comprehension []
print('Using list comprehension')
a = [hexStr[i:i+2] for i in range(0, len(hexStr), 2)]
# using next(a) will "consume" the item, so cannot "restart" a again from beginning.. 
# one way is convert to list, like so m=list(a)..
#print(next(a))
print(a)
print('\r\n')

lista = []
for k in a:
  #print(k)
  m = '0x' + k
  lista.append(m)

print(lista)  

print('\r\n')
print('using normal for loop')
listb = []
for n in range(0, len(hexStr), 2):
  listb.append(hexStr[n:n+2])

print(listb)

# Generator expression
print('\r\n')
print('Using Generator expression')
h = (hexStr[i:i+2] for i in range(0, len(hexStr), 2))
print(h) # will print <generator object <genexpr> at 0x00000000xxxxxxxx>
print('\r\n')

listh = []
for k in h:
  #print(k)
  m = '0x' + k
  listh.append(m)

print(listh)  

sys.exit()

#-------------------------------------------------------
# split into 8 pairs of hexcode..
hexby8 = '\n'.join(hexStr[i:i+16] for i in range(0, len(hexStr), 16))

formatted_by8 = list(hexby8.split())
print(formatted_by8)
a = []
for elem in formatted_by8:
  # add '0x' to each hexcode
  a.append('0x' + ', 0x'.join(elem[i:i+2] for i in range(0, len(elem), 2)))

for i in a:
  print(i)


input()

formatted_hex = ' 0x'.join(hexStr[i:i+2] for i in range(0, len(hexStr), 2))

# add a '0x' to first pair of hexcode
formatted = "0x" + formatted_hex

hexlist = list(formatted.split())


# hexStr == '7465737431323334544553543536373861626364656667683132333435363738'
print(hexStr)
print(formatted_hex)
print(formatted)
print(hexlist)

print('{}'.format(hexStr))

# a = (hex[i:i+2] for i in range(0, len(hex), 2))

# print(list(a))
# print(a)





