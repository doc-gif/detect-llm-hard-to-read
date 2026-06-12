import os
import sys
import math
import bisect
from sys import stdin, stdout
from math import gcd, floor, sqrt, log
from collections import defaultdict,Counter
from bisect import bisect_left as bl, bisect_right as br
from itertools import combinations

sys.setrecursionlimit(100000000)

int_inp = lambda: int(input())  # integer input
strng = lambda: input().strip()  # string input
jn = lambda x, l: x.join(map(str, l))
strl = lambda: list(input().strip())  # list of strings as input
mul = lambda: map(int, input().strip().split())  # multiple integers as ipnut
mulf = lambda: map(float, input().strip().split())  # multiple floats as ipnut
seq = lambda: list(map(int, input().strip().split()))  # list of integers

ceil = lambda x: int(x) if (x == int(x)) else int(x) + 1  # celing function
ceildiv = lambda x, d: x // d if (x % d == 0) else x // d + 1

flush = lambda: stdout.flush()
stdstr = lambda: stdin.readline()
stdint = lambda: int(stdin.readline())
stdpr = lambda x: stdout.write(str(x))

mod = 998244353
max_val=sys.maxsize
def divisorofn(n):
    factors = [0] * (n + 1)

    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            factors[j] += 1
    return factors[n]

def solve():
    n=int_inp()
    res=0
    s=0
    for i in range(1,n+1):
        res=(s+divisorofn(i))%mod
        s=(s+res)%mod
    print(res)





solve()