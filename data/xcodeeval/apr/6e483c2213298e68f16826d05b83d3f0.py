import queue
from math import *
import sys
from collections import *
from random import *

sys.setrecursionlimit(99999)
eps = sys.float_info.epsilon
P = 31
MOD = 10**9+7

def is_prime(n):
    if n == 0 or n == 1:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def div_up(n, k):
    if n % k == 0:
        return n // k
    else:
        return n // k + 1


def bfs(start, visited, graph):
    q = deque()
    visited[start] = True
    q.appendleft(start)
    while len(q) != 0:
        v = q.pop()
        for to in graph[v]:
            if not visited[to]:
                visited[to] = True
                q.appendleft(to)


def to_int(c):
    if c == '>':
        return 0
    return 1


def ford_bellman(edges, d, cost, n):
    for i in range(n - 1):
        flag = True
        for edge in edges:
            v, u = edge[0], edge[1]
            temp = d[v] + cost[edge]
            if temp < d[u]:
                d[u] = temp
                flag = False
        if flag:
            break


def num_len(n, base):
    if n == 0:
        return 1
    return int(floor(log(n, base) + 1))


cycles = 0
def dfs(graph, cl, p, v):
    global cycles
    cl[v] = 1
    for to in graph[v]:
        if cl[to] == 1 and p[v] != to:
            cycles += 1
        elif cl[to] == 0:
            p[to] = v
            dfs(graph, cl, p, to)
    cl[v] = 2


def down(a):
    for i in range(1, len(a)):
        if a[i] > a[i - 1]:
            return False
    return True


def up(a):
    for i in range(1, len(a)):
        if a[i] < a[i - 1]:
            return False
    return True


def _hash_(s):
    res = 0
    for i in range(len(s)):
        res += (ord(s[i]) - ord('a')) * P**i
    return res


def binpow(a, n):
    res = 1
    while n:
        if n & 1:
            res *= a
            res %= MOD
        a *= a
        a %= MOD
        n >>= 1
    return res


def solve():
    n, k = map(int, input().split())
    S = binpow(2, n - 1)
    if k == 0:
        print(1)
        return
    dp_eq = [1 for i in range(k + 1)]
    dp_big = [1 for i in range(k + 1)]
    dp_eq[1] = S
    if n % 2 != 0:
        dp_eq[1] += 1
    else:
        dp_eq[1] -= 1
    dp_big[1] = 0
    if n % 2 == 0:
        dp_big[1] += 1

    for i in range(2, k + 1):
        dp_eq[i] = dp_eq[i - 1] * dp_eq[1]
        dp_big[i] = dp_big[i - 1] * binpow(2, n) + dp_eq[i - 1] * dp_big[1]
    print(dp_eq[k] + dp_big[k])


for _ in range(int(input())):
    solve()


def debug():
    pass

# debug()
