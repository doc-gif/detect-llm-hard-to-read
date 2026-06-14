p = 10**9 + 7
import math


def inv(k, p):
    prod = 1
    while k > 1:
        prod *= p // k + 1
        k = (k * (p // k + 1)) % p
    return prod % p


n = int(input())
k = int(math.log2(n))
a = []
x = n
while x > 0:
    y = x // 2
    a.append(x - y)
    x = y
c = [sum(a[i:]) for i in range(k + 1)]
b = [n // (3 << i) - n // (6 << i) for i in range(k + 1)]
d = [n >> i - n // (3 << i) for i in range(k + 1)]
facs = [1] * (n + 1)
for i in range(2, n + 1):
    facs[i] = (i * facs[i - 1]) % p
if n < 3 * (1 << (k - 1)):
    start = k
else:
    start = 0
total = 0
for j in range(start, k + 1):
    prod = 1
    for i in range(j, k):
        prod *= b[i]
    prod *= d[j]
    for i in range(j):
        prod *= a[i]
    prod %= p
    prod = (prod * facs[n]) % p
    e = a[:j] + [d[j]] + b[j:k]
    f = [sum(e[: i + 1]) for i in range(k + 1)]
    g = 1
    for val in f:
        g *= val
    prod = (prod * inv(g, p)) % p
    total = (total + prod) % p
print(total)
