import sys

input = sys.stdin.buffer.readline
MOD = 998244353


def custom_print(val):
    sys.stdout.write(str(val) + "\n")


def choose(n, k):
    if k > n:
        return 0
    k = min(n - k, k)
    total = 1
    for i in range(n - k + 1, n + 1):
        total *= i
    for i in range(2, k + 1):
        total //= i
    return total % MOD


def factorial(n):
    total = 1
    for i in range(2, n + 1):
        total *= i
        total %= MOD
    return total


def place_rooks(n, k):
    if k == 0:
        return factorial(n)
    filled = n - k
    placements = 0
    for i in range(filled):
        mult = 1
        for _ in range(n):
            mult *= filled - i
            mult %= MOD
        term = ((-1) ** i) * choose(filled, i) * mult
        placements = (placements + term) % MOD
    total = (2 * choose(n, filled) * placements) % MOD
    if k == 0:
        total //= 2
    return total


n, k = map(int, input().split())
custom_print(place_rooks(n, k))
