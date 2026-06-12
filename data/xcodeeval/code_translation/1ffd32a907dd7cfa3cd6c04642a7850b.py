# coding: UTF-8
import sys
#sys.setrecursionlimit(n)
import heapq
import re
import bisect
import random
import math
import itertools
from collections import defaultdict, deque
from copy import deepcopy
from decimal import *

readl= lambda: list(map(str, sys.stdin.readline().split()))
readt= lambda: tuple(map(int, sys.stdin.readline().split()))
read = lambda: sys.stdin.readline().rstrip()
readi = lambda: int(read())
readmi = lambda: map(int, sys.stdin.readline().split())
readms = lambda: map(str, sys.stdin.readline().split())

t = readl()
n = []
m = []
t.sort()
for i in t:
    n.append(int(i[0]))
    m.append(i[1])
count = 2
if m[0] == m[1] == m[2]:
    if n[0] == n[1] == n[2] or (n[0] + 1 == n[1] and n[1] + 1 == n[2]):
        print(0)
    elif n[0] == n[1] or n[0] == n[2] or n[1] == n[2]:
        print(1)
    elif n[0] + 1 == n[1] or n[0] + 2 == n[1] or n[1] + 1 == n[2] or n[1] + 2 == n[2] or n[0] + 1 == n[2] or n[0] + 2 == n[2]:
        print(1)
    else:
        print(2)
elif m[0] == m[1]:
    if n[0] == n[1] or n[0] + 1 == n[1] or n[0] + 2 == n[1]:
        print(1)
    else:
        print(2)
elif m[0] == m[2]:
    if n[0] == n[2] or n[0] + 1 == n[2] or n[0] + 2 == n[2]:
        print(1)
    else:
        print(2) 
elif m[1] == m[2]:
    if n[1] == n[2] or n[1] + 1 == n[2] or n[1] + 2 == n[2]:
        print(1)
    else:
        print(2)
else:
    print(2)
