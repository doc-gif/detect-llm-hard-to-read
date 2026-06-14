n = int(input())
arr = [int(x) for x in input().strip().split()]
consecutive_groups = []
non_consecutive_set = set()
current_group = [arr[0]]
previous = arr[0]
for current in arr[1:]:
    if current == previous + 1:
        current_group.append(current)
    else:
        if len(current_group) >= 2:
            consecutive_groups.append(current_group)
        non_consecutive_set.add(current - previous + 1)
        current_group = [current]
    previous = current
if len(current_group) >= 2:
    consecutive_groups.append(current_group)
max_days = 0
for group in consecutive_groups:
    days = len(group) - 2
    if group[0] == 1:
        days += 1
    if group[-1] == 1000:
        days += 1
    max_days = max(max_days, days)
print(max_days)