from bisect import bisect_left as bl
from bisect import bisect_right as br
import heapq
import math
from collections import *
from functools import reduce,cmp_to_key
import sys
input = sys.stdin.readline
 
M = mod = 998244353
def factors(n):return sorted(list(set(reduce(list.__add__,([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))))
# def inv_mod(n):return pow(n, mod - 2, mod)
 
def li():return [int(i) for i in input().rstrip('\n').split()]
def st():return input().rstrip('\n')
def val():return int(input().rstrip('\n'))
def li2():return [i for i in input().rstrip('\n').split(' ')]
def li3():return [int(i) for i in input().rstrip('\n')]

def compare(a,b):
    if a[-1]<b[-1]:return -1
    elif a[-1]>b[-1]:return 1
    else:
        if sum(a[:-1]) > sum(b[:-1]):return -1
        return 1

t1, t2, x1, x2, t = li()
bestans = []
if t == t1 and t1 == t2:
    print(x1,x2)
elif t == t1:
    print(x1,0)

elif t == t2:
    print(0,x2)
else:

    r = (t2 - t)/(t - t1)


    for i in range(1,x2 + 1):
        curry1 = i*r
        if 0 <= int(curry1) <= x1:
            bestans.append([int(curry1),i,curry1 - int(curry1)])
        if 0 <= math.ceil(curry1) <= x1:
            bestans.append([math.ceil(curry1),i,math.ceil(curry1) - curry1])


    for i,(a,b,c) in enumerate(bestans):
        if ((a*t1 + b*t2)/(a + b)) < t:
            bestans[i][-1] = 1000
            continue
        bestans[i][-1] = abs(t - ((a*t1 + b*t2)/(a + b)))

    bestans.sort(key=cmp_to_key(compare))
    # print(bestans)
    print(*bestans[0][:-1])