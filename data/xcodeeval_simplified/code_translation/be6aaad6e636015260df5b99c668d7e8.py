import sys
def read_input():
    return sys.stdin.readline().strip()
dp = [[None] * 2001 for _ in range(50)]
n, s, k = map(int, read_input().split())
a = [None] * n
s -= 1
values = map(int, read_input().split())
for idx, val in enumerate(values):
    a[idx] = (val, idx)
colors = read_input()
for idx, ch in enumerate(colors):
    a[idx] += ("RGB".find(ch),)
a.sort()
result = 10**18
for i in range(n):
    current_dp = dp[i]
    current_value, current_pos, current_color = a[i]
    current_dp[current_value] = abs(s - current_pos)
    for j in range(i):
        prev_value, prev_pos, prev_color = a[j]
        if prev_color == current_color or prev_value == current_value:
            continue
        prev_dp = dp[j]
        for prev_sum in range(2001 - current_value):
            prev_cost = prev_dp[prev_sum]
            if prev_cost is not None:
                new_cost = prev_cost + abs(current_pos - prev_pos)
                new_sum = prev_sum + current_value
                if current_dp[new_sum] is None or current_dp[new_sum] > new_cost:
                    current_dp[new_sum] = new_cost
    for total in range(k, 2001):
        if current_dp[total] is not None:
            result = min(result, current_dp[total])
print(result if result != 10**18 else -1)