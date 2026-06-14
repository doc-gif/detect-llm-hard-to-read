n = int(input())
m = list(map(int, input().split()))
t = int(input())
m.sort()
if n == 1 or len(m) == 1:
    print(1)
elif m[-1] - m[0] <= t:
    print(n)
else:
    max_count = 1
    for i in range(n - 1):
        current_count = 1
        first_value = m[i]
        for j in range(i + 1, n):
            if m[j] - first_value <= t:
                current_count += 1
            else:
                break
        max_count = max(current_count, max_count)
    print(max_count)