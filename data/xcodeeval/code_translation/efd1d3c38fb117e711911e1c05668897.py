#!/usr/bin/env python3
from bisect import *

def ri():
    return map(int, input().split())

n, m = ri()

if m-n >= 0:
    print(n)
    exit()

k = (n-m)
al = 0
ar = 2*k*(k+1)+1

while ar-al > 1:
    a = (al+ar)//2
    aa = a*(a+1)//2
    if k <= aa:
        ar = a
    else:
        al = a
print(ar+m)
