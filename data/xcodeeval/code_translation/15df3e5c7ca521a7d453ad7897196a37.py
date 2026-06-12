mod = int(1e9+7)

def fast_power(base, exp):
    res = 1
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res 

n = int(input())
res = fast_power(2, 2*n-1) + fast_power(2, n-1)
print(1 if n == 0 else res % mod)
