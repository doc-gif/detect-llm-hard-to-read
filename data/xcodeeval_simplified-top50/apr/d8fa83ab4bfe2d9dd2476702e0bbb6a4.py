import math

n = int(input())
edges = [list(map(int, input().split())) for _ in range(n - 1)]
graph = {}
for x, y in edges:
    if x not in graph:
        graph[x] = []
    if y not in graph:
        graph[y] = []
    graph[x].append(y)
    graph[y].append(x)


def find_center(g):
    dist = {}
    dist[1] = 0
    queue = [(1, 0)]
    while queue:
        u, d = queue.pop(0)
        for v in g[u]:
            if v not in dist:
                dist[v] = d + 1
                queue.append((v, dist[v]))
    max_dist = -1
    start = None
    for u, d in dist.items():
        if d > max_dist:
            max_dist = d
            start = u
    dist = {}
    prev = {}
    dist[start] = 0
    queue = [(start, 0)]
    while queue:
        u, d = queue.pop(0)
        for v in g[u]:
            if v not in dist:
                prev[v] = u
                dist[v] = d + 1
                queue.append((v, dist[v]))
    max_dist = -1
    end = None
    for u, d in dist.items():
        if d > max_dist:
            max_dist = d
            end = u
    path = [end]
    while prev[path[-1]] != start:
        path.append(prev[path[-1]])
    return path[len(path) // 2]


root = find_center(graph)
parent = {}
subtree_size = {}
queue = [root]
parent[root] = -1
idx = 0
while idx < len(queue):
    u = queue[idx]
    for v in graph[u]:
        if parent[u] == v:
            continue
        parent[v] = u
        queue.append(v)
    idx += 1
for u in reversed(queue):
    subtree_size[u] = 1
    for v in graph[u]:
        if parent[u] == v:
            continue
        subtree_size[u] += subtree_size[v]
neighbors = [(u, subtree_size[u]) for u in graph[root]]
neighbors.sort(key=lambda x: x[1])
threshold = math.ceil((n - 1) / 3)
total = 0
group1 = []
group2 = []
i = 0
while total < threshold:
    group1.append(neighbors[i][0])
    total += neighbors[i][1]
    i += 1
while i < len(neighbors):
    group2.append(neighbors[i][0])
    i += 1


def assign_weights(u, weights, edge_weights):
    if subtree_size[u] == 1:
        return
    cur = 0
    for v in graph[u]:
        if v == parent[u]:
            continue
        first = weights[cur]
        edge_weights.append((u, v, first))
        next_weights = [w - first for w in weights[cur + 1 : cur + subtree_size[v]]]
        assign_weights(v, next_weights, edge_weights)
        cur += subtree_size[v]


size_a = sum(subtree_size[x] for x in group1)
size_b = sum(subtree_size[x] for x in group2)
arr1 = list(range(1, size_a + 1))
arr2 = [i * (size_a + 1) for i in range(1, size_b + 1)]
edge_weights = []
cur = 0
for u in group1:
    first = arr1[cur]
    edge_weights.append((root, u, first))
    next_weights = [w - first for w in arr1[cur + 1 : cur + subtree_size[u]]]
    cur += subtree_size[u]
    assign_weights(u, next_weights, edge_weights)
cur = 0
for u in group2:
    first = arr2[cur]
    edge_weights.append((root, u, first))
    next_weights = [w - first for w in arr2[cur + 1 : cur + subtree_size[u]]]
    cur += subtree_size[u]
    assign_weights(u, next_weights, edge_weights)
for u, v, w in edge_weights:
    print(f"{u} {v} {w}")
