import operator as op
import math
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

n,m,t=map(int,input().split())
ways=0
a=4
b=t-a
while(a<=n and b!=0):
	if(b<=m):
		ways+=ncr(n,a)*ncr(m,b)
	a=a+1
	b=t-a
print(int(ways))
	
	

