import sys
input = sys.stdin.readline
# sys.setrecursionlimit(400000)
def I(): return input().strip()
def II(): return int(input().strip())
def LI(): return [*map(int, input().strip().split())]
import copy, string, math, time, functools, fractions
from heapq import heappush, heappop, heapify
from bisect import bisect_left, bisect_right
from collections import deque, defaultdict, Counter, OrderedDict
from itertools import permutations, chain, combinations, groupby
from operator import itemgetter
from types import GeneratorType  # for recursion
from typing import Iterable, TypeVar, Union  # for sorted set


for _ in range(1):
    inp = list(I())
    n = len(inp)
    if inp == ['0']:
        print(1)
        continue
    if n < 2:
        print(0)
        continue
    if n < 3:
        if list('__') == inp or list('_X') == inp or list('X_') == inp:
            print(3)
        elif list('XX') == inp:
            print(0)
        elif list('_5') == inp or list('X5') == inp:
            print(2)
        elif list('_0') == inp or list('X0') == inp:
            print(1)
        elif list('2_') == inp or list('5_') == inp or list('7_') == inp or list('2X') == inp or list('5X') == inp or list('7X') == inp:
            print(1)
        elif list('25') == inp or list('50') == inp or list('75') == inp:
            print(1)
        else:
            print(0)
        continue
    ans = 0
    r = 9
    if 'X' not in inp:
        r = 1
    for x in range(r):
        temp = copy.deepcopy(inp)
        for i in range(n):
            if temp[i] == 'X':
                temp[i] = str(x)
        if temp[0] == '0':
            continue
        var = 1
        if temp[-1] == temp[-2] == '_':
            var *= 4
        elif temp[-1] == '_':
            if not (temp[-2] == '0' or temp[-2] == '2' or temp[-2] == '5' or temp[-2] == '7'):
                continue
        elif temp[-2] == '_':
            if not (temp[-1] == '0' or temp[-1] == '5'):
                continue
            var *= 2
        else:
            if not ((temp[-2] == '0' and temp[-1] == '0') or (temp[-2] == '2' and temp[-1] == '5') or (temp[-2] == '5' and temp[-1] == '0') or (temp[-2] == '7' and temp[-1] == '5')):
                continue
        # print(temp)
        if temp[0] == '_':
            var *= 9
        for i in range(1, n - 2):
            if temp[i] == '_':
                var *= 10
        ans += var
    print(ans)
    
