s = input().split()
x, y, m = (int(i) for i in s)
ans = 0
if x >= m or y >= m:
    print(0)
elif x <= 0 and y <= 0:
    print(-1)
else:
    if x < 0:
        steps = abs(x // y)
        ans += steps
        x += y * steps
    elif y < 0:
        steps = abs(y // x)
        ans += steps
        y += x * steps
    while x < m and y < m:
        ans += 1
        if x < y:
            x += y
        else:
            y += x
    print(ans)