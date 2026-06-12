def gcd(a, b):
    if a % b == 0:
        return b
    else:
        return gcd(b, a % b)


t1, t2, x1, x2, t0 = map(int, input().split())
a = t2 - t0
b = t0 - t1
if a == 0:
    y1, y2 = 0, x2
    print(y1, y2)
    exit(0)
if b == 0:
    y1, y2 = x1, 0
    print(y1, y2)
    exit(0)
g = gcd(a, b)
a //= g
b //= g
if a <= x1 and b <= x2:
    mintime = min(x1 // a, x2 // b)
    print(mintime * a, mintime * b)
    exit(0)
y1 = 1
y2 = 1
min_diff = 99999
while y1 <= x1 and y2 <= x2:
    if y1 / y2 < a / b:
        diff = a / b - y1 / y2
        if diff < min_diff:
            min_diff = diff
            miny1, miny2 = y1, y2
        y1 += 1
    else:
        y2 += 1
y1, y2 = miny1, miny2
mintime = min(x1 // y1, x2 // y2)
print(mintime * y1, mintime * y2)
