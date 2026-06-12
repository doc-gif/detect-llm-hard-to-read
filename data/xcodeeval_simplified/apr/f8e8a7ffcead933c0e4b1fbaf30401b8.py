import sys

range = xrange
input = raw_input
MOD = 998244353
import __pypy__

modmul = __pypy__.intop.int_mulmod
mod_mul = lambda a, b: modmul(a, b, MOD)
mod_pow = lambda a, b: pow(a, b, MOD)
MAX = 10**6 + 10
modinv = [1] * MAX
for i in range(2, MAX):
    modinv[i] = mod_mul(-(MOD // i), modinv[MOD % i])
fac = [1]
for i in range(1, MAX):
    fac.append(mod_mul(fac[-1], i))
invfac = [1]
for i in range(1, MAX):
    invfac.append(mod_mul(invfac[-1], modinv[i]))


def choose(n, k):
    return mod_mul(mod_mul(fac[n], invfac[k]), invfac[n - k])


def parity_sign(x):
    return -1 if x & 1 else 1


n = int(input())
ans = 0
for i in range(1, n + 1):
    base = -mod_pow(3, n - i)
    tmp = mod_pow(base + 1, n) - mod_pow(base, n)
    ans += parity_sign(i + 1 + n) * mod_mul(choose(n, i), tmp)
extra = 0
for i in range(1, n + 1):
    extra += parity_sign(i + 1) * mod_mul(choose(n, i), mod_pow(3, n * (n - i) + i))
print(3 * ans + 2 * extra) % MOD
