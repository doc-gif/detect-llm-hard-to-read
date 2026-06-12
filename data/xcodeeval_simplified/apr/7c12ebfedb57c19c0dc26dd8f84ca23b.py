n = int(input())
points = []
x_vals = []
y_vals = []
for _ in range(4 * n + 1):
    x, y = map(int, input().split())
    points.append((x, y))
    x_vals.append(x)
    y_vals.append(y)
left = min(x_vals)
right = max(x_vals)
down = min(y_vals)
up = max(y_vals)
if right - left == up - down:
    for x, y in points:
        if x_vals.count(x) == 1 and y_vals.count(y) == 1:
            print(x, y)
            break
    for x, y in points:
        if left < x < right and down < y < up:
            print(x, y)
            break
else:
    for x, y in points:
        if x_vals.count(x) == 1 and y_vals.count(y) == 1:
            print(x, y)
            break
    for x, y in points:
        if x_vals.count(x) == 1 and (x == left or x == right):
            print(x, y)
            break
        elif y_vals.count(y) == 1 and (y == up or y == down):
            print(x, y)
            break
