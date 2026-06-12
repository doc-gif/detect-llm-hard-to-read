from fractions import Fraction

g = [0] * 111111
t = [0] * 111111
prime = [0] * 111111
pm = [0] * 111111
for i in range(len(prime)):
    prime[i] = {}


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def ksm(a, b, p=int(1e9 + 7)):
    a = a % p
    ans = 1
    while b > 0:
        if b & 1:
            ans = ans * a % p
        b = b >> 1
        a = a * a % p
    return ans


def get_ck(m, n):
    ans = 0

    def get_fac():
        for i in range(2, 100011):
            if pm[i] == 0:
                prime[i][i] = 1
                for j in range(2, 100001 // i + 1):
                    pm[i * j] = 1
                    prime[i * j][i] = 1

    if prime[m] == {}:
        get_fac()
    prime_list = list(prime[m].keys())
    for i in range(1, 1 << len(prime_list)):
        t_val = i
        rongchixishu = -1
        lcm = 1
        index = len(prime_list) - 1
        while t_val > 0:
            if t_val & 1:
                lcm = lcm * prime_list[index]
                rongchixishu *= -1
            t_val >>= 1
        ans += n // lcm * rongchixishu
    return ans


m = int(input())
p = int(1e9 + 7)
tmp = ksm(m, p - 2)
for j in range(m, 0, -1):
    c1 = 0
    tyouce = tmp
    gyouce = 0
    if j == 1:
        c1 = 0
    else:
        c1 = m // j * tmp % p
    for k in range(2, m // j + 1):
        ck = (m // j - get_ck(k, m // j) + p) % p
        ck = ck * tmp % p
        tyouce = (tyouce + ck * t[k * j]) % p
        gyouce = (gyouce + ck * (t[k * j] + g[k * j])) % p
    t[j] = tyouce * ksm(1 - c1 + p, p - 2) % p
    gyouce = (gyouce + tmp + c1 * t[j]) % p
    g[j] = gyouce * ksm(1 - c1 + p, p - 2) % p
print(g[1])
