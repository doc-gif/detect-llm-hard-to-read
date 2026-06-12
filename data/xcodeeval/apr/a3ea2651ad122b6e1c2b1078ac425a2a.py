def prime(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return 0
    return 1


def binpow(x, y, mod):
    if y == 0:
        return 1
    if y == -1:
        return 1. / x
    p = binpow(x, y // 2, mod)
    p *= p
    if y % 2:
        p *= x
    return p % mod

mod = 998244353
n, m = map(int, input().split())
out = 0
for i in range(1, 1 + n):
    out += pow(m, i, mod)
cnt = 1
minu = 1
for i in range(1, 1 + n):
    if cnt > m:
        break
    if prime(i):
        cnt *= i
    minu *= (m // cnt)
    minu %= mod
    out -= minu

print(out)
