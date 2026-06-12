import math
n = int(input())

if n%2==0:
	l=n/2
else:
	l=(n+1)/2

max_value=0

a1=0
b1=0

for i in range(int(l)):
	a = i
	b = n-i

	if math.gcd(a,b)!=1:
		continue

	elif a/b>max_value:
		max_value=a/b
		a1=a
		b1=b

print (a1 , b1)
