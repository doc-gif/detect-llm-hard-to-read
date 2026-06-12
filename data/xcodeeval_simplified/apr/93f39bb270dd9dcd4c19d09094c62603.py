import sys

MOD = 1000000007


def read_line():
    return sys.stdin.readline().strip()


def read_int():
    return int(read_line())


def read_ints():
    return map(int, read_line().split())


n = read_int()
points = [0] * n
x_to_indices = {}
y_to_indices = {}
for i in range(n):
    a = tuple(read_ints())
    points[i] = a
    x_to_indices.setdefault(a[0], []).append(i)
    y_to_indices.setdefault(a[1], []).append(i)
result = 1
queue = [0] * n
visited = [True] * n
queue_left = 0
queue_right = 0
for i in range(n):
    if visited[i]:
        visited[i] = False
        queue[queue_right] = i
        queue_right += 1
        component_start = queue_left
        edge_count = 0
        x_set = set()
        y_set = set()
        while queue_left < queue_right:
            v = queue[queue_left]
            queue_left += 1
            a = points[v]
            x_set.add(a[0])
            y_set.add(a[1])
            for u in x_to_indices[a[0]]:
                edge_count += 1
                if visited[u]:
                    visited[u] = False
                    queue[queue_right] = u
                    queue_right += 1
            for u in y_to_indices[a[1]]:
                edge_count += 1
                if visited[u]:
                    visited[u] = False
                    queue[queue_right] = u
                    queue_right += 1
        vertex_count = queue_left - component_start
        if vertex_count * 3 - 1 == edge_count:
            result = (result * (pow(2, vertex_count + 1, MOD) - 1)) % MOD
        else:
            result = (result * pow(2, len(x_set) + len(y_set), MOD)) % MOD
print(result)
