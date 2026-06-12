from sys import stdin
from itertools import combinations
n, l, r, x = map(int, stdin.readline().split())
problems = list(map(int, stdin.readline().split()))
ans = 0
for k in range(2, n + 1):
    for combo in combinations(problems, k):
        sorted_combo = sorted(combo)
        total = sum(sorted_combo)
        if sorted_combo[-1] - sorted_combo[0] >= x and l <= total <= r:
            ans += 1
print(ans)