def prime(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return 0
        i += 1
    return 1


def binpow(x, y, mod):
    if y == 0:
        return 1
    if y == -1:
        return 1.0 / x
    p = binpow(x, y // 2, mod)
    p *= p
    if y % 2:
        p *= x
    return p % mod


MOD = 998244353
n, m = map(int, input().split())
total = 0
for i in range(1, n + 1):
    total += pow(m, i, MOD)
cnt = 1
subtract_term = 1
for i in range(1, n + 1):
    if cnt > m:
        break
    if prime(i):
        cnt *= i
    subtract_term = (subtract_term * (m // cnt)) % MOD
    total -= subtract_term
print(total)
