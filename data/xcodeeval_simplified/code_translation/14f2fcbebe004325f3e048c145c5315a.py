a, b, c = map(int, input().split())
if abs(a - b) <= 1:
    result = a + b + 2 * c
else:
    if a < b:
        result = 2 * a + 1 + 2 * c
    else:
        result = 2 * b + 1 + 2 * c
print(result)