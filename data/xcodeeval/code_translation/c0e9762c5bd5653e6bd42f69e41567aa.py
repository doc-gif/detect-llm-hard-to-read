from decimal import *
import math

getcontext().prec = 1000000


inputs = [int(x) for x in input().split()]
a = inputs[0]
b = inputs[1]
c = inputs[2]

num = Decimal(a)/Decimal(b)

d = str(num)
found = False
where = 0

pos = -2

at = 0

#print(d) 
for _ in d:
	if ( at == 999999 ):
		break
	#print(_)
	if _ == '.':
		found = True
		where = at
		continue
	if found == False:
		continue
	if _ == str(c):
		pos = at - where
		break
	at = at + 1

if ( pos == -2 and c == 0 and at < 999999 ):
	pos = at
print(pos + 1)

