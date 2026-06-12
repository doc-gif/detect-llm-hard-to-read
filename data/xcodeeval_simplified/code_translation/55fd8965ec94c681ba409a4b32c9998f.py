from itertools import permutations
ii = lambda: int(input())
mi = lambda: map(int, input().split())
li = lambda: list(mi())
l = [li() for _ in range(5)]
indices = [0, 1, 2, 3, 4]
max_sum = 0
for a, b, c, d, e in permutations(indices, 5):
    pair_sum = (
        l[a][b]
        + l[b][a]
        + l[b][c]
        + l[c][b]
        + 2 * (l[c][d] + l[d][c] + l[d][e] + l[e][d])
    )
    max_sum = max(max_sum, pair_sum)
print(max_sum)