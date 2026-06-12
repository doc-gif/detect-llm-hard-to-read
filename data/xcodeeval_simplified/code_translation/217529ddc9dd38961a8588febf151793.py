c, d = map(int, input().split())
n, m = map(int, input().split())
k = int(input())
z = 0
best = 10**10
while True:
    required = n * m - k - z * n
    best = min(best, z * c + max(required, 0) * d)
    if required < 0:
        break
    z += 1
print(best)