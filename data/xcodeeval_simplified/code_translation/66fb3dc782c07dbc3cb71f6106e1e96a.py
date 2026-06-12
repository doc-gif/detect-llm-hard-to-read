n, k = map(int, input().split())
remainder_seen = [0] * k
for _ in range(k):
    remainder = n % k
    if remainder == 0:
        exit(print("Yes"))
    if remainder_seen[remainder]:
        exit(print("No"))
    remainder_seen[remainder] = 1
    n += remainder
print("Yes")