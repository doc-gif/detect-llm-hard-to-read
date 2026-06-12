n = int(input())
disjoint_set = [-1] * n


def root(x, level=200):
    if disjoint_set[x] < 0:
        return x
    if level < 1:
        while disjoint_set[x] >= 0:
            x = disjoint_set[x]
        return x
    disjoint_set[x] = root(disjoint_set[x], level - 1)
    return disjoint_set[x]


def join(x, y):
    r1, r2 = root(x), root(y)
    if r1 == r2:
        return
    disjoint_set[r2] = r1


points = []
vertical_points = {}
horizontal_points = {}
for i in range(n):
    x, y = map(int, input().split())
    points.append((x, y))
    if x in vertical_points:
        join(i, vertical_points[x])
    else:
        vertical_points[x] = i
    if y in horizontal_points:
        join(i, horizontal_points[y])
    else:
        horizontal_points[y] = i
sets = {}
for i in range(n):
    r = root(i)
    if r in sets:
        sets[r].append(points[i])
    else:
        sets[r] = [points[i]]
MOD = 10**9 + 7
ans = 1
for s in sets.values():
    xs = [x for x, y in s]
    ys = [y for x, y in s]
    unique_count = len(set(xs)) + len(set(ys))
    if unique_count <= len(s):
        ans *= 2**unique_count
    else:
        ans *= 2**unique_count - 1
    ans %= MOD
print(ans % MOD)
