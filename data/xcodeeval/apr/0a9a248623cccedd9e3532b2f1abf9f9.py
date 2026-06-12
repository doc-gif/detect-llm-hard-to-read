n, m, k, xx, yy = map(int, input().split())
if n != 1:
    plus = k // ((n * 2 - 2) * m)
    k %= (n * 2 - 2) * m
else:
    plus = 0
l = [[plus * 2 for p in range(m)] for pp in range(n)]
for t in range(m):
    l[0][t] -= plus
    l[-1][t] -= plus
x = y = s = 0
d = 1
for t in range(k):
    l[x][y] += 1
    if y == m-1:
        y = 0
        if x+d == -1:
            d = -d
            x += d
        elif x+d == n:
            d = -d
            x += d
        else:
            x += d
        if x == -1:
            x = 0
        if x == n:
            x = n-1
    else:
        y += 1
print(max(max(l, key=lambda tt: max(tt))), min(min(l, key=lambda tt: min(tt))), l[xx-1][yy-1])