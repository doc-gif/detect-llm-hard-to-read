"""
Oh, Grantors of Dark Disgrace, 
Do Not Wake Me Again.
"""

ii = lambda: int(input())
mi = lambda: map(int, input().split())
li = lambda: list(mi())
si = lambda: input()

from itertools import permutations

l = [[]]*5
n = [0, 1, 2, 3, 4]

for i in range(5):
    l[i] = li()

maxi = 0

for a, b, c, d, e in permutations(n, 5):
    s = l[a][b] + l[b][a] + l[b][c] + l[c][b] + 2*(l[c][d] + l[d][c] + l[d][e] + l[e][d])
    maxi = max(maxi, s)

print(maxi)