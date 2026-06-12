# -*- coding: utf-8 -*-

import sys
from collections import Counter

def input(): return sys.stdin.readline().strip()
def list2d(a, b, c): return [[c] * b for i in range(a)]
def list3d(a, b, c, d): return [[[d] * c for j in range(b)] for i in range(a)]
def list4d(a, b, c, d, e): return [[[[e] * d for j in range(c)] for j in range(b)] for i in range(a)]
def ceil(x, y=1): return int(-(-x // y))
def INT(): return int(input())
def MAP(): return map(int, input().split())
def LIST(N=None): return list(MAP()) if N is None else [INT() for i in range(N)]
def Yes(): print('Yes')
def No(): print('No')
def YES(): print('YES')
def NO(): print('NO')
INF = 10 ** 18
MOD = 10 ** 9 + 7

def bfs(src, S, K):
    from collections import deque

    que = deque([(src)])
    res = set()
    while que:
        s = que.popleft()
        res.add(s)
        if len(res) == K:
            return res
        for i in range(len(s)):
            t = s[:i] + s[i+1:]
            if t in res:
                continue
            que.append(t)
    return res

N, K = MAP()
S = input()

res = bfs(S, S, K)
if len(res) < K:
    print(-1)
else:
    ans = 0
    for s in res:
        ans += N - len(s)
    print(ans)
