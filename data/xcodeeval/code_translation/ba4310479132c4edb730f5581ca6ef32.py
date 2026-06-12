g, v = [input() for i in range(8)], [8, 8]
for i in range(8):
    for j in range(8):
        if g[i][j] == 'W' and all(g[k][j] == '.' for k in range(i)):
            v[0] = min(v[0], i)
        elif g[i][j] == 'B' and all(g[k][j] == '.' for k in range(i + 1, 8)):
            v[1] = min(v[1], 7 - i)
print('A' if v[0] <= v[1] else 'B')