from math import *

N = 400020
ar = []
for i in range(0,N):
	x = 0
	b = 5
	while b<=i:
		x += i//b
		b *= 5
	ar.append(x)

n = int(input())

sol = [ i for i in range(0,N) if ar[i]==n ]
print(len(sol))
print(*sol)

#  C:\Users\Usuario\HOME2\Programacion\ACM