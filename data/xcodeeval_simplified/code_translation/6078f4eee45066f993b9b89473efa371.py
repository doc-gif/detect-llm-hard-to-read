from math import gcd
MOD = 998244353
n, m = map(int, input().split())
ans = 0
cur = m
g = 2
q = m * m
for i in range(2, n + 1):
    if gcd(g, i) == 1 and g < 10**13:
        g *= i
    cur = (cur * (m // g)) % MOD
    ans = (ans + q - cur) % MOD
    q = (q * m) % MOD
print(ans % MOD)