x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
 
if x1 == x2:
    x1 += 1
elif y1 == y2:
    y1 += 1
print((abs(x2 - x1) + 1 + abs(y2 - y1) + 1) * 2)