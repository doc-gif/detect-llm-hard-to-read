import math
n, k = map(int, input().split())

diffs = []
for i in range(1, math.ceil(math.sqrt(n)) + 1):
    if n % i == 0:
        a = i*k + (n//i)
        b = k*(n//i) + i
        if (a // k) * (a % k) == n:
            diffs.append(a)
        if (b // k) * (b % k) == n:
            diffs.append(b)

# print(diffs)
ans = min(diffs)
print(ans)