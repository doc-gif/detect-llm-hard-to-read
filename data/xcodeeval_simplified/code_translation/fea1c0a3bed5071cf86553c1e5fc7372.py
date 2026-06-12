n, k = map(int, input().split())
a = list(map(int, input().split()))
c = 0
for i in range(n):
    if a[i] > k:
        break
    c += 1
d = 0
if c != n:
    for i in range(n):
        if a[n - i - 1] > k:
            break
        d += 1
print(c + d)