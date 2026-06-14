def play(t1, t2):
    if t1[0] > t2[1] and t1[1] > t2[0]:
        return 1
    if t1[0] < t2[1] and t1[1] < t2[0]:
        return -1
    return 0
p = [tuple(map(int, input().split())) for _ in range(4)]
m = [(p[0][0], p[1][1]), (p[1][0], p[0][1]), (p[2][0], p[3][1]), (p[3][0], p[2][1])]
res = [(play(m[0], m[2]), play(m[0], m[3])), (play(m[1], m[2]), play(m[1], m[3]))]
best_score = max(max(pair) for pair in res)
filtered = [pair for pair in res if max(pair) == best_score]
min_scores = [min(pair) for pair in filtered]
if 1 in min_scores:
    rr = 2
else:
    rr = max(min_scores) + 1
results = ["Team 2", "Draw", "Team 1"]
print(results[rr])