n = list(map(int, input().split()))
a, b = n[0], n[1]
print(a - 1 if b == 1 else a * (b - 1))