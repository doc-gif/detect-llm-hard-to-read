x1, y1, x2, y2 = map(int, input().split())
x, y = map(int, input().split())
dx = abs(x1 - x2)
dy = abs(y1 - y2)
if x == 0:
    print("YES" if dy % y == 0 else "NO")
    exit()
if y == 0:
    print("YES" if dx % x == 0 else "NO")
    exit()
x_steps = dx // x
y_steps = dy // y
print("YES" if (dx % x == 0 and dy % y == 0 and x_steps % 2 == y_steps % 2) else "NO")