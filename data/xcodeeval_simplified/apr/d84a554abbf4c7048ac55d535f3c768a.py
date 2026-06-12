import math

n = int(input())
if n == 1:
    print()
else:
    edges = [list(map(int, input().split())) for _ in range(n - 1)]
    graph = {}
    for x, y in edges:
        if x not in graph:
            graph[x] = []
        if y not in graph:
            graph[y] = []
        graph[x].append(y)
        graph[y].append(x)

    def find_center(graph):
        dist = {}
        dist[1] = 0
        queue = [(1, 0)]
        while queue:
            u, d = queue.pop(0)
            for v in graph[u]:
                if v not in dist:
                    dist[v] = d + 1
                    queue.append((v, dist[v]))
        farthest_node = None
        max_dist = -1
        for node, d in dist.items():
            if d > max_dist:
                max_dist = d
                farthest_node = node
        dist = {}
        parent = {}
        dist[farthest_node] = 0
        queue = [(farthest_node, 0)]
        while queue:
            u, d = queue.pop(0)
            for v in graph[u]:
                if v not in dist:
                    parent[v] = u
                    dist[v] = d + 1
                    queue.append((v, dist[v]))
        farthest_node = None
        max_dist = -1
        for node, d in dist.items():
            if d > max_dist:
                max_dist = d
                farthest_node = node
        path = [farthest_node]
        while parent[path[-1]] != farthest_node:
            path.append(parent[path[-1]])
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
    root_children = [(child, subtree_size[child]) for child in graph[root]]
    root_children.sort(key=lambda x: x[1])
    threshold = math.ceil((n - 1) / 3)
    group1 = []
    group2 = []
    total = 0
    i = 0
    while total < threshold:
        group1.append(root_children[i][0])
        total += root_children[i][1]
        i += 1
    while i < len(root_children):
        group2.append(root_children[i][0])
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
            new_weights = [w - first for w in weights[cur + 1 : cur + subtree_size[v]]]
            assign_weights(v, new_weights, edge_weights)
            cur += subtree_size[v]

    size_group1 = sum(subtree_size[x] for x in group1)
    size_group2 = sum(subtree_size[x] for x in group2)
    weights1 = list(range(1, size_group1 + 1))
    weights2 = [i * (size_group1 + 1) for i in range(1, size_group2 + 1)]
    edge_weights = []
    cur = 0
    for u in group1:
        first = weights1[cur]
        edge_weights.append((root, u, first))
        new_weights = [w - first for w in weights1[cur + 1 : cur + subtree_size[u]]]
        cur += subtree_size[u]
        assign_weights(u, new_weights, edge_weights)
    cur = 0
    for u in group2:
        first = weights2[cur]
        edge_weights.append((root, u, first))
        new_weights = [w - first for w in weights2[cur + 1 : cur + subtree_size[u]]]
        cur += subtree_size[u]
        assign_weights(u, new_weights, edge_weights)
    for u, v, w in edge_weights:
        print(f"{u} {v} {w}")
