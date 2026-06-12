g = [0] * 111111
t = [0] * 111111


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def ksm(a, b, p=int(1e9 + 7)):
    a %= p
    ans = 1
    while b > 0:
        if b & 1:
            ans = ans * a % p
        b >>= 1
        a = a * a % p
    return ans


MOD = int(1e9 + 7)
m = int(input())
inv_m = ksm(m, MOD - 2)
for j in range(m, 0, -1):
    c1 = 0
    tyouce = inv_m
    gyouce = 0
    if j == 1:
        c1 = 0
    else:
        c1 = (m // j) * inv_m % MOD
    for k in range(2, m // j + 1):
        t0 = m // j // k
        t1 = 0
        for l in range(1, k):
            if gcd(l, k) == 1:
                t1 += 1
        ck = t0 * t1 % MOD
        for l in range(1, (m // j) % k + 1):
            if gcd(l, k) == 1:
                ck += 1
        ck = ck * inv_m % MOD
        tyouce = (tyouce + ck * t[k * j]) % MOD
        gyouce = (gyouce + ck * (t[k * j] + g[k * j])) % MOD
    denominator = (1 - c1 + MOD) % MOD
    t[j] = tyouce * ksm(denominator, MOD - 2) % MOD
    gyouce = (gyouce + inv_m + c1 * t[j]) % MOD
    g[j] = gyouce * ksm(denominator, MOD - 2) % MOD
print(g[1])
