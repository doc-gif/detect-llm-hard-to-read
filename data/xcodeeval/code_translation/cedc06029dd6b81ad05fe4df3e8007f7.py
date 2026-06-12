#n = int(input())
#n, m = map(int, input().split())
#d = list(map(int, input().split()))

n, h, m = map(int, input().split())
res = [h for i in range(n)]

for i in range(m):
    l, r, x = map(int, input().split())
    for j in range(l-1, r):
        res[j] = min(res[j], x)

print(sum([x**2 for x in res]))
