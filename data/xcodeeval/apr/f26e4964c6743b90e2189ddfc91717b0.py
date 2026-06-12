import math

def ok(xa, ya):
    x, y = xb - xa, yb - ya
    d = math.gcd(abs(xc), abs(yc))
    if xc == 0:
        return x % yc == 0 and y % yc == 0
    if yc == 0:
        return x % xc == 0 and y % xc == 0
    if (x % d != 0) or (y % d != 0):
        return 0
    a, b, c1, c2 = xc // d, yc // d, x // d, -y // d
    if a == 0 and b == 0:
        return c1 == 0 and c2 == 0
    if (c1 * b + c2 * a) % (a * a + b * b) != 0:
        return 0
    yy = (c1 * b + c2 * a) / (a * a + b * b)
    if a != 0:
        return (c1 - b * yy) % a == 0
    else:
        return (c2 - a * yy) % b == 0


xa, ya = map(int,input().split())
xb, yb = map(int,input().split())
xc, yc = map(int,input().split())
if xc == 0 and yc == 0:
    if xa == xb and ya == yb:
        print('YES')
    else:
        print('NO')
    exit(0)
if ok(xa, ya) or ok(-ya, xa) or ok(-xa, -ya) or ok(ya, -xa):
    print('YES')
else:
    print('NO')
