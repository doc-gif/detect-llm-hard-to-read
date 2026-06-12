n, s, k = map(int, input().split())
radii = list(map(int, input().split()))
radii.append(0)
colors = input()
adjacency = []
for i in range(n + 1):
    neighbors = {}
    for j in range(n):
        if i == n:
            neighbors[j] = abs((s - 1) - j)
        else:
            if colors[i] != colors[j] and radii[i] < radii[j]:
                neighbors[j] = abs(i - j)
    adjacency.append(neighbors)
memory = [{} for _ in range(n + 1)]


def get_min_cost(start, remaining_k):
    if memory[start].get(remaining_k):
        return memory[start].get(remaining_k)
    if radii[start] >= remaining_k:
        memory[start][remaining_k] = 0
    else:
        best = None
        for neighbor in adjacency[start]:
            neighbor_cost = get_min_cost(neighbor, remaining_k - radii[start])
            if neighbor_cost is None:
                continue
            current = neighbor_cost + adjacency[start][neighbor]
            if best is None or current < best:
                best = current
        if best is not None:
            memory[start][remaining_k] = best
    return memory[start].get(remaining_k)


result = get_min_cost(n, k)
print(result if result is not None else -1)
