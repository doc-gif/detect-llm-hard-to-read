def frange(start, stop, step=1):
    while start < stop:
        yield start
        start += step


x1, y1, x2, y2 = map(int, input().split())
x3, y3, x4, y4 = map(int, input().split())
x5, y5, x6, y6 = map(int, input().split())
x3 = max(x3, x1)
x5 = max(x5, x1)
y3 = max(y3, y1)
y5 = max(y5, y1)
x4 = min(x4, x2)
x6 = min(x6, x2)
y4 = min(y4, y2)
y6 = min(y6, y2)
a = {(x, y) for x in frange(x1, x2) for y in frange(y1, y2)}
b = {(x, y) for x in frange(x3, x4) for y in frange(y3, y4)}
a -= b
v = {(x, y) for x in frange(x5, x6) for y in frange(y5, y6)}
a -= v
print("YES" if a else "NO")
