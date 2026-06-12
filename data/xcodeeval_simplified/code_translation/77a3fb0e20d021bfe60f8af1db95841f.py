n, m = map(int, input().split())
a = list(map(int, input().split()))
max_rounds = current_round = 0
result_index = 0
for i in range(n):
    required_rounds = (a[i] + m - 1) // m
    if current_round <= required_rounds:
        current_round = required_rounds
        result_index = i
print(result_index + 1)