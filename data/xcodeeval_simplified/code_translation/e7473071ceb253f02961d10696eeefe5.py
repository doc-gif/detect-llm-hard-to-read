k, n, w = map(int, input().split())
total_cost = ((2 * k + k * (w - 1)) * w) // 2
if total_cost > n:
    print(total_cost - n)
else:
    print(0)