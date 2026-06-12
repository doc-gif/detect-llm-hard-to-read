#!/usr/bin/env python3
# from typing import *

import sys
import io
import math
import collections
import decimal
import itertools
import bisect
import heapq


def input():
    return sys.stdin.readline()[:-1]


sys.setrecursionlimit(1000000)

# _INPUT = """8935891487501725 71487131900013807
# """
# sys.stdin = io.StringIO(_INPUT)

INF = 10**10

YES = 'YES'
NO = 'NO'

def dfs(s, SY):
    if s == SY:
        return True
    n = int(s)
    if n in ng:
        return False
    if len(s) > 100:
        return False
    ng.add(n)
    # print(n)
    for s1 in [str(int(s[::-1])), (s+'1')[::-1]]:
        if s1 in ng:
            continue
        if dfs(s1, SY):
            return True
    return False


ng = set()

def solve(X, Y):
    if X == Y:
        return 'YES'
    
    SX = bin(X)[2:]
    SY = bin(Y)[2:]

    if dfs(SX, SY):
        return 'YES'

    return 'NO'

X, Y = map(int, input().split())
print(solve(X, Y))