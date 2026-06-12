n = int(input())
graph = [{}, {}, {}]
for i in range(n):
    for j in range(n):
        row_and_col = [(k, j) for k in range(n)] + [(i, k) for k in range(n)]
        row_and_col.remove((i, j))
        row_and_col.remove((i, j))
        graph[0][(i, j)] = row_and_col
        graph[1][(i, j)] = []
        for k in range(n):
            for l in range(n):
                if abs(k - i) == abs(l - j) != 0:
                    graph[1][(i, j)].append((k, l))
        graph[2][(i, j)] = []
        for k in range(n):
            for l in range(n):
                if {abs(k - i), abs(l - j)} == {1, 2}:
                    graph[2][(i, j)].append((k, l))
dists = [[{}, {}, {}], [{}, {}, {}], [{}, {}, {}]]
for i in range(n):
    for j in range(n):
        for k in range(3):
            dists[k][k][(i, j, i, j)] = 0
for i in range(n):
    for j in range(n):
        for k in range(3):
            layers = [[(i, j, k, 0)], [], [], [], []]
            for l in range(4):
                for guy in layers[l]:
                    cur_r, cur_c, cur_piece, cur_swaps = guy
                    for m in range(3):
                        if m != cur_piece:
                            state = (i, j, cur_r, cur_c)
                            if state not in dists[k][m]:
                                layers[l + 1].append((cur_r, cur_c, m, cur_swaps + 1))
                                dists[k][m][state] = 1000 * (l + 1) + cur_swaps + 1
                    for boi in graph[cur_piece][(cur_r, cur_c)]:
                        state = (i, j, boi[0], boi[1])
                        if state not in dists[k][cur_piece]:
                            layers[l + 1].append((boi[0], boi[1], cur_piece, cur_swaps))
                            dists[k][cur_piece][state] = 1000 * (l + 1) + cur_swaps
                        elif 1000 * (l + 1) + cur_swaps < dists[k][cur_piece][state]:
                            layers[l + 1].append((boi[0], boi[1], cur_piece, cur_swaps))
                            dists[k][cur_piece][state] = 1000 * (l + 1) + cur_swaps
locs = [None] * (n * n)
for i in range(n):
    row = list(map(int, input().split()))
    for j in range(n):
        locs[row[j] - 1] = (i, j)
best = (0, 0, 0)
for idx in range(n * n - 1):
    cur_r, cur_c = locs[idx]
    nxt_r, nxt_c = locs[idx + 1]
    state = (cur_r, cur_c, nxt_r, nxt_c)
    new0 = min(
        best[0] + dists[0][0][state],
        best[1] + dists[1][0][state],
        best[2] + dists[2][0][state],
    )
    new1 = min(
        best[0] + dists[0][1][state],
        best[1] + dists[1][1][state],
        best[2] + dists[2][1][state],
    )
    new2 = min(
        best[0] + dists[0][2][state],
        best[1] + dists[1][2][state],
        best[2] + dists[2][2][state],
    )
    best = (new0, new1, new2)
ans = min(best)
print(ans // 1000, ans % 1000)