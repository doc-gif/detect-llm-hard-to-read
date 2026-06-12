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
    return list(map(lambda x: int(x) - 1, input().split()))


def getArray(intn):
    return [int(input()) for i in range(intn)]


MOD = 998244353
N, M = getNM()
prime_set = {2}
max_val = 100000
limit = int(math.sqrt(max_val))
data = [i + 1 for i in range(2, max_val, 2)]
while limit > data[0]:
    prime_set.add(data[0])
    data = [j for j in data if j % data[0] != 0]
prime_set.update(data)
l = 1
all_prod = 1
subs_prod = 1
ans = 0
for i in range(N):
    if i + 1 in prime_set and l <= M:
        l *= i + 1
    subs_prod = (subs_prod * (M // l)) % MOD
    all_prod *= M
    ans = (ans + all_prod - subs_prod) % MOD
print(ans)
