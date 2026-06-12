tracking = sorted(list(map(int, input().split())))
x, y, z = tracking
if x * 2 >= y and y * 2 >= z:
    result = x + y + z
else:
    result = (tracking[0]+tracking[1]) * 2
print(result)