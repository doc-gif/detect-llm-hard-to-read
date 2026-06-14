n = int(input()) * 2
arr = sorted(int(x) for x in input().split())
x = arr[n - 1]
for i in range(n):
    for j in range(i + 1, n):
        a, q = 0, 0
        for h in range(n):
            if h == i or h == j:
                continue
            if q % 2 == 0:
                a -= arr[h]
            else:
                a += arr[h]
            q += 1
        x = min(x, a)
print(x)