
Read = lambda:map(int, input().split())
from functools import reduce

def init():
    g = [[False] * (n + 1) for _ in range(n + 1)]
    for _ in range(m):
        x, y = Read()
        g[x][y] = g[y][x] = True
    return g

def solve():
    color = [0 for _ in range(n+1)]
    g = init()
    for i in range(1, n + 1):
        if reduce(lambda x, y : x and y, g[i][1:i] + g[i][i + 1:]):
            color[i] = 2    # 'b'

    for u in range(1, n + 1):
        if not color[u]:
            color[u] = 1   # 'a'
            for v in range(1, n + 1):
                if u != v and g[u][v] and not color[v]:
                    color[v] = 1
            break

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                continue
            if g[i][j] and color[i] + color[j] == 1:
                return 'No'
            if not g[i][j] and color[i] == color[j]:
                return 'No'

    def judge(x):
        if x == 1:
            return 'a'
        elif x == 2:
            return 'b'
        else:
            return 'c'
    return 'Yes\n' + ''.join(map(judge, color[1:]))


if __name__ == '__main__':
    while True:
        try:
            n, m = Read()
        except:
            break

        print(solve())
