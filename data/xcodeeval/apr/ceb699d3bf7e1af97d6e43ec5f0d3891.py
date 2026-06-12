from collections import defaultdict, deque, Counter
import sys
from decimal import *
from heapq import heapify, heappop, heappush
import math
import random
import string
from copy import deepcopy
from itertools import combinations, permutations, product
from operator import mul, itemgetter
from functools import reduce, lru_cache
from bisect import bisect_left, bisect_right

def input():
    return sys.stdin.readline().rstrip()
def getN():
    return int(input())
def getNM():
    return map(int, input().split())
def getList():
    return list(map(int, input().split()))
def getListGraph():
    return list(map(lambda x:int(x) - 1, input().split()))
def getArray(intn):
    return [int(input()) for i in range(intn)]

mod = 10 ** 9 + 7
MOD = 998244353

# import pypyjit
# pypyjit.set_param('max_unroll_recursion=-1')
inf = float('inf')
eps = 10 ** (-12)
dy = [0, 1, 0, -1]
dx = [1, 0, -1, 0]

#############
# Main Code #
#############

prime = [2]
max = 100000
limit = int(math.sqrt(max))
data = [i + 1 for i in range(2, max, 2)]

while limit > data[0]:
    prime.append(data[0])
    data = [j for j in data if j % data[0] != 0]
prime = set(prime + data)

N, M = getNM()
l, all, subs = 1, 1, 1
ans = 0
for i in range(N):
    if i + 1 in prime and l <= M:
        l *= (i + 1)
    subs = (subs * (M // l)) % MOD
    all *= M
    ans %= MOD
    ans += all - subs
    ans %= MOD
print(ans)