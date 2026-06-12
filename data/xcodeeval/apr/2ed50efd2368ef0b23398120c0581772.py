
def frange(start, stop, step=1):
    while start<stop:
        yield start
        start+=step

x1,y1,x2,y2 = list(map(int, input().split(" ")))
x3,y3,x4,y4 = list(map(int, input().split(" ")))
x5,y5,x6,y6 = list(map(int, input().split(" ")))

if x3 < x1:
    x3 = x1
if x5 < x1:
    x5 = x1

if y3 < y1:
    y3 = y1
if y5 < y1:
    y5 = y1

if x4 > x2:
    x4 = x2
if x6 > x2:
    x6 = x2

if y4 > y2:
    y4 = y2
if y6 > y2:
    y6 = y2


a = {(x, y) for x in frange(x1, x2) for y in frange(y1, y2)}
b = {(x, y) for x in frange(x3, x4) for y in frange(y3, y4)}
a = a - b
del b
v = {(x, y) for x in frange(x5, x6) for y in frange(y5, y6)}
a = a - v



if len(a):
    print("YES")
else:
    print("NO")
