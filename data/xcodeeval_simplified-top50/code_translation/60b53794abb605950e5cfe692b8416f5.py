import sys
n, m = map(int, input().split())
d = [input() for _ in range(n)]
r = 0
for i in range(n):
    for j in range(m):
        right = d[i][min(j + 1, m - 1)]
        left = d[i][max(0, j - 1)]
        up = d[max(0, i - 1)][j]
        down = d[min(n - 1, i + 1)][j]
        neighbors = right + left + up + down
        if d[i][j] == "W" and "P" in neighbors:
            r += 1
print(r)