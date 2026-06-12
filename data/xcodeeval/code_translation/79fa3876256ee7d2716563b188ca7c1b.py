n, a = map(int, input().split())

if a % 2 == 1:
    print((a + 1) // 2)
else:
    print(n // 2 - a // 2 + 1)
