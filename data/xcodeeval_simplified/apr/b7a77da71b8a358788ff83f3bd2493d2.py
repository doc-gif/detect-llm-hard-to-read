import sys
import itertools
from collections import defaultdict

factorials = [1] * 19
for i in range(1, 19):
    factorials[i] = i * factorials[i - 1]


def cumsum(l):
    for i in range(1, len(l)):
        l[i] += l[i - 1]


def enum(lst):
    global K, S
    d = defaultdict(lambda: [0] * (K + 1))
    for opts in itertools.product((0, 1, 2), repeat=len(lst)):
        s = 0
        marks = 0
        for i, opt in enumerate(opts):
            if s > S:
                break
            if opt == 1:
                s += lst[i]
            elif opt == 2:
                if lst[i] <= 18:
                    s += factorials[lst[i]]
                    marks += 1
                else:
                    s = S + 1
        if s <= S:
            d[s][marks] += 1
    return d


n, K, S = map(int, sys.stdin.next().split())
l = sorted(map(int, sys.stdin.next().split()))
mid = len(l) // 2
p1 = enum(l[:mid][::-1])
p2 = enum(l[mid:][::-1])
variants = 0
for s in p1:
    target = S - s
    if target in p2:
        m1 = p1[s]
        m2 = p2[target]
        for k1, c1 in enumerate(m1):
            for k2, c2 in enumerate(m2):
                if k1 + k2 <= K:
                    variants += c1 * c2
print(variants)
