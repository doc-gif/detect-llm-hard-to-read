def read_ints():
    return map(int, input().split())
n, m = read_ints()
if m >= n:
    print(n)
    exit()
k = n - m
low = 0
high = 2 * k * (k + 1) + 1
while high - low > 1:
    mid = (low + high) // 2
    triangular = mid * (mid + 1) // 2
    if k <= triangular:
        high = mid
    else:
        low = mid
print(high + m)