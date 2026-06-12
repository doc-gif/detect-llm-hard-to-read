

g = [0]*111111
t = [0]*111111


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def ksm(a, b, p=int(1e9+7)):
    a = a % p
    ans = 1
    while b > 0:
        if b & 1:
            ans = ans * a % p
        b = b >> 1
        a = a*a % p
    return ans


m = int(input())
p = int(1e9+7)
tmp = ksm(m, p-2)
for j in range(m, 0, -1):
    c1 = 0
    tyouce = tmp
    gyouce = 0
    if j == 1:
        c1 = 0
    else:
        c1 = m//j * tmp % p

    for k in range(2, m//j + 1):
        t0 = m//j//k
        t1 = 0
        for l in range(1, k):
            if gcd(l, k) == 1:
                t1 += 1
        ck = t0*t1 % p
        for l in range(1, (m//j) % k + 1):
            if gcd(l, k) == 1:
                ck += 1
        ck = ck*tmp%p
        tyouce = (tyouce + ck * t[k*j]) % p
        gyouce = (gyouce + ck * (t[k*j] + g[k*j])) % p
    t[j] = tyouce * ksm(1-c1+p, p-2) % p
    gyouce = (gyouce + tmp + c1 * t[j]) % p
    g[j] = gyouce * ksm(1-c1+p, p-2) % p

# print(t[2])
# print(g[2])
# print(t[1])
print(g[1])
