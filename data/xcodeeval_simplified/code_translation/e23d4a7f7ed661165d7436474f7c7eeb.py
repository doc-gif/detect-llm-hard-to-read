n, m = map(int, input().split())
edges = [[] for _ in range(n)]
for _ in range(m):
    a, b = map(int, input().split())
    a, b = a - 1, b - 1
    edges[a].append(b)
    edges[b].append(a)
if n <= 6:
    print(m)
else:
    intersections = []
    for i in range(n):
        for j in range(i):
            common = set(edges[i]) & set(edges[j])
            intersections.append(common)
    common_counts = [len(s) for s in intersections]
    print(m - min(common_counts))