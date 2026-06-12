def inp(dtype=str, strip=True):
    s = input()
    res = [dtype(p) for p in s.split()]
    res = res[0] if len(res) == 1 and strip else res
    return res


def problem1():

    def test(cur, steps):
        if 0 < cur <= n and cur not in a:
            return steps
        else:
            return -1

    t = inp(int)
    for _ in range(t):
        n, s, k = inp(int)
        a = inp(int, strip=False)
        a = set(a)

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
        r = r - 1
        c = c - 1

        if state[r][c] == 0:
            state[r][c] = 1
            q = 1 - r
            if c - 1 >= 0 and state[q][c - 1] == 1:
                nconflicts += 1
                conflicts[r][c][-1 + 1] = 1
                conflicts[q][c - 1][1 + 1] = 1
            if state[q][c] == 1:
                nconflicts += 1
                conflicts[r][c][0 + 1] = 1
                conflicts[q][c][0 + 1] = 1
            if c + 1 < n and state[q][c + 1] == 1:
                nconflicts += 1
                conflicts[r][c][1 + 1] = 1
                conflicts[q][c + 1][-1 + 1] = 1
        else:
            state[r][c] = 0
            q = 1 - r
            if c - 1 >= 0 and state[q][c - 1] == 1:
                nconflicts -= 1
                conflicts[r][c][-1 + 1] = 0
                conflicts[q][c - 1][1 + 1] = 0
            if state[q][c] == 1:
                nconflicts -= 1
                conflicts[r][c][0 + 1] = 0
                conflicts[q][c][0 + 1] = 0
            if c + 1 < n and state[q][c + 1] == 1:
                nconflicts -= 1
                conflicts[r][c][1 + 1] = 0
                conflicts[q][c + 1][-1 + 1] = 0

        if nconflicts == 0:
            print("YES")
        else:
            print("NO")


def problem4():

    def dist(xi, yi, xj, yj):
        return abs(xi - xj)  + abs(yi - yj)

    def dist2(xi, yi, xj, yj):
        return 2 * max(abs(xi - xj), abs(yi - yj))

    x0, y0, ax, ay, bx, by = inp(int)
    xs, ys, t = inp(int)

    i = 0
    a = [(x0, y0)]
    xmin, ymin = x0, y0
    while i < 60:
        xmin = ax * xmin + bx
        ymin = ay * ymin + by
        a.append((xmin, ymin))

    i = 0
    xmin, ymin = x0, y0
    while dist2(xs, ys, xmin, ymin) > t and i < 60:
        xmin = ax * xmin + bx
        ymin = ay * ymin + by
        i += 1
    imin = i

    xmax, ymax = xmin, ymin
    while dist2(xs, ys, xmax, ymax) <= t and i < 60:
        xmax = ax * xmax + bx
        ymax = ay * ymax + by
        i += 1
    imax = i - 1

    res = 0
    for istart in range(imin, imax + 1):
        dist_start = dist(xs, ys, *a[istart])
        if dist_start > t:
            continue

        # some down and all up
        for imed in range(imin, istart + 1):
            dist_med = dist(*a[istart], *a[imed])
            if dist_start + dist_med > t:
                continue

            i = imed + 1
            while dist_start + dist_med + dist(*a[imed], *a[i]) <= t:
                i += 1

            i = max(imed, i - 1)
            res = max(res, i - imed + 1)

        # some up and all down
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


if __name__ == '__main__':
    # problem1()
    # problem2()
    # problem3()
    problem4()
    # problem5()
