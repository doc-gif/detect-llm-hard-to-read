from math import gcd
a,b = map(int,input().split(' '))
gcd = gcd(a,b)
a,b = a/gcd, b/gcd
if abs(a-b) <= 1: print('Equal')
elif a < b: print('Dasha')
else: print('Masha')