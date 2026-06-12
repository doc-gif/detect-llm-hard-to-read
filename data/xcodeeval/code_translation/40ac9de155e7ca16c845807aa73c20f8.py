from sys import stdin
from itertools import combinations
n, l, r , x = map(int, stdin.readline().rstrip().split(" "))
li = list(map(int, stdin.readline().rstrip().split(" ")))
z = []
ans = 0
for i in range(2, n+1):
    z += list(combinations(li, i))

for i in z:
    a = sorted(i)
    if a[-1]-a[0]>=x and r >= sum(a) >= l:
        ans+=1

print(ans)