def gcd(a, b):
    if b == 0:
        return a, 1, 0
    d, x_, y_ = gcd(b, a % b)
    return d, y_, x_ - (a // b) * y_
def co(a, i):
    return (f[a] * g[i] % 998244353 * g[a - i]) % 998244353
MOD = 998244353
MAX_N = 5005
a, b, c = map(int, input().split())
f = [1]
for i in range(1, MAX_N):
    f.append(f[-1] * i % MOD)
g = [gcd(val, MOD)[1] for val in f]
r = 0
for i in range(min(a, b) + 1):
    r = (r + co(a, i) * co(b, i) % MOD * f[i]) % MOD
h = 0
for i in range(min(a, c) + 1):
    h = (h + co(a, i) * co(c, i) % MOD * f[i]) % MOD
v = 0
for i in range(min(c, b) + 1):
    v = (v + co(c, i) * co(b, i) % MOD * f[i]) % MOD
print((r * h * v) % MOD)