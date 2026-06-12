a, b, c = map(int, input().split())
if abs(a - b) <= 1:
    print(a + b + 2 * c)
else:
    if a < b:
        print(a + a + 1 + 2 * c)
    else:
        print(b + b + 1 + 2 * c)

