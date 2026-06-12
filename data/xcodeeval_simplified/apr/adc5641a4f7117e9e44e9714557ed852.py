from sys import stdin, stdout
import sys

sys.setrecursionlimit(1500)
MOD = 998244353
faca = [0, 1]


def fac(n):
    if len(faca) > n:
        return faca[n]
    r = n * fac(n - 1)
    faca.append(r)
    return r


def com(p1, p2):
    return fac(p1) // fac(p1 - p2) // fac(p2)


def isprime(n):
    j = 2
    while j * j <= n:
        if n % j == 0:
            return False
        j += 1
    return True


def modular_stability(n, k):
    if k > n:
        return 0
    if k == 1:
        return n
    res = com(n - 1, k - 1) % MOD
    for i in range(2, n + 1):
        cnt = n // i
        if cnt == k:
            res += 1
        elif cnt > k:
            res += com(cnt - 1, k - 1)
            res %= MOD
    return res


if __name__ == "__main__":
    n, k = map(int, stdin.readline().split())
    for i in range(1, n + 1):
        fac(i)
    print(modular_stability(n, k))
