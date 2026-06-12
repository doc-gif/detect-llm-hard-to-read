import sys
import bisect
import copy

input = sys.stdin.readline
n, m = map(int, input().split())
K = [0] + list(map(int, input().split()))
SP = [list(map(int, input().split())) for _ in range(m)]
SP2 = [[] for _ in range(n + 1)]
for d, t in SP:
    SP2[t].append(d)
for lst in SP2:
    lst.sort()
total_needed = sum(K)
min_day = total_needed
max_day = total_needed * 2
max_bought = 0
for day in range(min_day, max_day + 1):
    last_sale_day_for_item = [[] for _ in range(day + 1)]
    for i in range(n + 1):
        idx = bisect.bisect_right(SP2[i], day) - 1
        if idx >= 0:
            last_sale_day_for_item[SP2[i][idx]].append(i)
    gold = 0
    bought = 0
    remaining = copy.deepcopy(K)
    for d in range(1, day + 1):
        gold += 1
        for t in last_sale_day_for_item[d]:
            can_buy = min(remaining[t], gold)
            remaining[t] -= can_buy
            gold -= can_buy
            bought += can_buy
    max_bought = max(max_bought, bought)
print(max_day - max_bought)
