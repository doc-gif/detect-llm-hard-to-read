first = second = draw = 0
z, x = map(int, input().split())
for i in range(1, 7):
    if abs(i - z) < abs(i - x):
        first += 1
    elif abs(i - z) > abs(i - x):
        second += 1
    else:
        draw += 1
print(first, draw, second)