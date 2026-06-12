n, m = map(int, input().split())
a = list(map(int, input().split()))

ans = r = 0
for i in range(n) :
    x = a[i]
    if (r <= (x + m - 1) // m) :
        r = (x + m - 1) // m
        ans = i

print(ans + 1)
