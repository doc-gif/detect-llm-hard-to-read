def inp(dtype=str, strip=True):
    s = input()
    res = [dtype(p) for p in s.split()]
    if len(res) == 1 and strip:
        return res[0]
    return res


def problem1():
    def test(cur, steps):
        if 0 < cur <= n and cur not in a:
            return steps
        return -1

    t = inp(int)
    for _ in range(t):
        n, s, k = inp(int)
        a = set(inp(int, strip=False))
        res = -1
        steps = 0
        while res < 0:
            res = test(s + steps, steps)
            if res < 0:
                res = test(s - steps, steps)
            steps += 1
        print(res)


def problem2():
    n = inp(int)
    res = 0
    for i in range(1, n + 1):
        res += 1 / i
    print(res)


def problem3():
    n, q = inp(int)
    conflicts = [[[0, 0, 0] for _ in range(n)] for _ in range(2)]
    state = [[0 for _ in range(n)] for _ in range(2)]
    nconflicts = 0
    for _ in range(q):
        r, c = inp(int)
        r -= 1
        c -= 1
        q = 1 - r
        if state[r][c] == 0:
            state[r][c] = 1
            if c - 1 >= 0 and state[q][c - 1] == 1:
                nconflicts += 1
                conflicts[r][c][0] = 1
                conflicts[q][c - 1][2] = 1
            if state[q][c] == 1:
                nconflicts += 1
                conflicts[r][c][1] = 1
                conflicts[q][c][1] = 1
            if c + 1 < n and state[q][c + 1] == 1:
                nconflicts += 1
                conflicts[r][c][2] = 1
                conflicts[q][c + 1][0] = 1
        else:
            state[r][c] = 0
            if c - 1 >= 0 and state[q][c - 1] == 1:
                nconflicts -= 1
                conflicts[r][c][0] = 0
                conflicts[q][c - 1][2] = 0
            if state[q][c] == 1:
                nconflicts -= 1
                conflicts[r][c][1] = 0
                conflicts[q][c][1] = 0
            if c + 1 < n and state[q][c + 1] == 1:
                nconflicts -= 1
                conflicts[r][c][2] = 0
                conflicts[q][c + 1][0] = 0
        print("YES" if nconflicts == 0 else "NO")


def problem4():
    def dist(xi, yi, xj, yj):
        return abs(xi - xj) + abs(yi - yj)

    def dist2(xi, yi, xj, yj):
        return 2 * max(abs(xi - xj), abs(yi - yj))

    x0, y0, ax, ay, bx, by = inp(int)
    xs, ys, t = inp(int)
    a = [(x0, y0)]
    x, y = x0, y0
    for _ in range(60):
        x = ax * x + bx
        y = ay * y + by
        a.append((x, y))
    i = 0
    x, y = x0, y0
    while dist2(xs, ys, x, y) > t and i < 60:
        x = ax * x + bx
        y = ay * y + by
        i += 1
    imin = i
    x, y = x, y
    while dist2(xs, ys, x, y) <= t and i < 60:
        x = ax * x + bx
        y = ay * y + by
        i += 1
    imax = i - 1
    res = 0
    for istart in range(imin, imax + 1):
        dist_start = dist(xs, ys, *a[istart])
        if dist_start > t:
            continue
        for imed in range(imin, istart + 1):
            dist_med = dist(*a[istart], *a[imed])
            if dist_start + dist_med > t:
                continue
            i = imed + 1
            while dist_start + dist_med + dist(*a[imed], *a[i]) <= t:
                i += 1
            i = max(imed, i - 1)
            res = max(res, i - imed + 1)
        for imed in range(istart, imax + 1):
            dist_med = dist(*a[istart], *a[imed])
            if dist_start + dist_med > t:
                continue
            i = imed - 1
            while dist_start + dist_med + dist(*a[imed], *a[i]) <= t:
                i -= 1
            i = min(imed, i + 1)
            res = max(res, imed - i + 1)
    print(res)


def problem5():
    pass


if __name__ == "__main__":
    problem4()
