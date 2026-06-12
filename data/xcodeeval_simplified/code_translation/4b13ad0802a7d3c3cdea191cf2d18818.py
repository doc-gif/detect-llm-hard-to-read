n = int(input())
l = list(map(int, input().split()))
costs = []
for i in range(n):
    total_cost = 0
    for j in range(n):
        if j <= i:
            total_cost += l[j] * i * 4
        else:
            total_cost += l[j] * j * 4
    costs.append(total_cost)
print(min(costs))