# -*- coding: utf-8 -*-

import math
import collections
import bisect
import heapq
import time
import random
import itertools
import sys

"""
created by shhuan at 2017/12/2 22:13

"""


f0 = "What are you doing at the end of the world? Are you busy? Will you save us?"


MAXN = 10**5+5
F = [0] * MAXN
F[0] = len(f0)

p1 = "What are you doing while sending \""
p2 = "\"? Are you busy? Will you send \""
p3 = "\"?"
lp1, lp2, lp3 = len(p1), len(p2), len(p3)
l = lp1 + lp2 + lp3

for i in range(0, MAXN-1):
    F[i+1] = 2 * F[i] + l
    # s[i+1] = p1 + si + p2 + si + p3


def solve(n, k):
    if n == 0:
        if k > len(f0):
            return '.'
        return f0[k-1]

    if k <= lp1:
        return p1[k-1]
    elif k <= lp1 + F[n-1]:
        return solve(n-1, k-len(p1))
    elif k <= lp1 + F[n-1] + lp2:
        return p2[k-lp1-F[n-1]-1]
    elif k <= lp1 + lp2 + 2*F[n-1]:
        return solve(n-1, k-lp1-lp2-F[n-1])
    elif k <= lp1 + lp2 + 2*F[n-1] + lp3:
        return p3[k-lp1-lp2-2*F[n-1]-1]
    else:
        return '.'






Q = int(input())

ans = ""
for i in range(Q):
    N, K = map(int, input().split())
    ans += solve(N, K)

print(ans)