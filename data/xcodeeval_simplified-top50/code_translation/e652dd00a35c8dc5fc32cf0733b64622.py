a, b = map(int, input().split())
def count_ones(x):
    count = 0
    while x > 0:
        count += x % 2
        x //= 2
    return count
if b == 0:
    print(count_ones(a))
    exit(0)
for n in range(1, 100):
    j = n * b
    if a <= j:
        break
    elif count_ones(a - j) <= n and a - j >= n:
        print(n)
        exit(0)
print(-1)