from collections import Counter, defaultdict, deque
import bisect
import dbm
import sys
import os
from itertools import repeat, permutations
import itertools
import math
import heapq
import random
from sys import stdin, stdout

MOD = 998244353
from io import BytesIO, IOBase

BUFSIZE = 8192


def inp(force_list=False):
    re = list(map(int, input().split()))
    if len(re) == 1 and not force_list:
        return re[0]
    return re


def inst():
    return input().strip()


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def lcm(x, y):
    return x * y // gcd(x, y)


def qmod(a, b, mod=MOD):
    res = 1
    while b:
        if b & 1:
            res = (res * a) % mod
        b >>= 1
        a = (a * a) % mod
    return res


def inv(a):
    return qmod(a, MOD - 2)


def query(tp, l, r=0):
    if tp == 1:
        print("? 1 %d" % (l + 1,))
        stdout.flush()
        return inst()
    else:
        if r < l:
            return 0
        print("? 2 %d %d" % (l + 1, r + 1))
        stdout.flush()
        return inp()


fac = [1]
for i in range(1, 100001):
    fac.append((fac[-1] * i) % MOD)


def C(n, k):
    return fac[n] * inv((fac[k] * fac[n - k]) % MOD) % MOD


def lstr(da):
    return " ".join(map(str, da))


IMX = int(1e16 + 7)


def my_main():
    kase = 1
    for ik in range(kase):
        n, k = inp()
        ans = 0
        for i in range(min(n, k) + 1):
            ans += C(n, i)
            ans %= MOD
        print(ans)


my_main()
