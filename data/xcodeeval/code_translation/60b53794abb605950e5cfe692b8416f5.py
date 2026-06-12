import math
import sys

#n = int(input())
#n, m = map(int, input().split())
#d = list(map(int, input().split()))

n, m = map(int, input().split())
d = []
for i in range(n):
    d.append(input())

r = 0
for i in range(n):
    for j in range(m):
        t = d[i][min(j+1,m-1)] + d[i][max(0, j-1)] + d[max(0, i-1)][j] +d[min(n-1, i+1)][j]
        if d[i][j] == 'W' and 'P' in t:
            r += 1
print(r)

