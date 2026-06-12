import sys
range = xrange
input = raw_input
import __pypy__
mulmod = __pypy__.intop.int_mulmod

MOD = 10**9+7
n, k = [int(x) for x in input().split()]

def f(n):
    s = 0
    for i in range(n):
        s += pow(i,k,MOD)
        s %= MOD
    return s

precalc = [0]
for i in range(k + 1):
    precalc.append((precalc[-1] + pow(i,k,MOD)) % MOD)

def interpolate(samples, x):
    x %= MOD
    m = len(samples)
    if x < m:
        return samples[x]
    
    modinv = [1]*m
    for i in range(2, m):
        modinv[i] = mulmod(-(MOD//i), modinv[MOD%i], MOD)

    invfac = [1]
    for i in range(1, m):
        invfac.append(mulmod(invfac[-1], modinv[i], MOD))
    invneg_fac = [invfac[i] * (1 - 2 * (i & 1)) for i in range(m)]

    xfac_down = [1]
    for j in reversed(range(x - (m - 1), x + 1)):
        xfac_down.append(xfac_down[-1] * j)
    
    xfac_up = [1]
    for j in range(x - (m - 1), x + 1):
        xfac_up.append(xfac_up[-1] * j)
    
    s = 0
    for i in range(m):
        pr = precalc[i]
        #pr = mulmod(pr, pow(x - i, MOD - 2, MOD), MOD)
        pr = mulmod(pr, xfac_down[i] * xfac_up[m - 1 - i] % MOD, MOD)
        pr = mulmod(pr, mulmod(invneg_fac[m - i - 1], invfac[i], MOD), MOD)
        s = (s + pr) % MOD
    return s
print (interpolate(precalc, n + 1) - (k == 0)) % MOD
