import sys

sys.setrecursionlimit(100000000)
MOD = 998244353


def divisorofn(n):
    factors = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            factors[j] += 1
    return factors[n]


def solve():
    n = int(input())
    res = 0
    s = 0
    for i in range(1, n + 1):
        res = (s + divisorofn(i)) % MOD
        s = (s + res) % MOD
    print(res)


solve()
