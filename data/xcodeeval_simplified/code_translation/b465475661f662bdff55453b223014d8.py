tracking = sorted(map(int, input().split()))
x, y, z = tracking
result = (x + y + z) if (x * 2 >= y and y * 2 >= z) else (tracking[0] + tracking[1]) * 2
print(result)