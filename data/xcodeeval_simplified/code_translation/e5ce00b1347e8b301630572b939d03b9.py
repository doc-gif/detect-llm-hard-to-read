from functools import reduce
n, k, m = map(int, input().split())
t = sorted(map(int, input().split()))
total_time = reduce(lambda x, y: x + y, t)
max_tasks = 0
full_sets = 0
while full_sets <= n and full_sets * total_time <= m:
    completed = full_sets * k + full_sets
    remaining_time = m - total_time * full_sets
    for time_per_task in t:
        tasks = min(n - full_sets, remaining_time // time_per_task)
        completed += tasks
        remaining_time -= tasks * time_per_task
    max_tasks = max(max_tasks, completed)
    full_sets += 1
print(max_tasks)