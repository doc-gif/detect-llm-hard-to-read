a, b = map(int, input().split())
x = abs((b - 1) - a)
print(int((a - x) / 2) if x < a else 0)