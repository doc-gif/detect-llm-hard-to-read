mod = 1000000007
def power(base, exponent):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2
    return result
n, m = map(int, input().split())
n += 1
res = power(n * 2, m - 1) * (n - m) * 2
print(res % mod)