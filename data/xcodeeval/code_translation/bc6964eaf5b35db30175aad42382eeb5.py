x, k = [int(a) for a in input().strip().split()]


def binpow(x, k, mod):
    res = 1
    while k > 0:
        if k & 1:
            res  = ( res * x ) % mod
        x = ( x * x) % mod
        k >>= 1
    return res
if x == 0:
    print(0)
    exit()

mod = int(1e9 + 7)
k2 = binpow(2, k, mod)
res = ( k2 * (2 * x - 1) + 1) % mod

res %= mod

print(int(res))