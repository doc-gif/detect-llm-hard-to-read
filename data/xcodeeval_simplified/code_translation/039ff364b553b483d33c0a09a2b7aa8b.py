import math
def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0
a, aa, b, bb, l, r = [int(x) for x in input().split()]
g, x, y = xgcd(a, b)
c = bb - aa
if c % g != 0:
    print(0)
    exit(0)
i = a * (x * c) // g + aa
ii = (-b * (y * c) // g) + bb
step = a * b // g
if (ii - i) % step != 0:
    print(0)
    exit(0)
if i > max(aa, bb):
    i -= ((i - max(aa, bb)) // step) * step
elif i < max(aa, bb):
    diff = max(aa, bb) - i
    i += (diff // step + (1 if diff % step != 0 else 0)) * step
f = (l - i) // step
if (l - i) % step != 0:
    f += 1
f = max(f, 0)
s = (r - i) // step
print(max(0, s - f + 1))