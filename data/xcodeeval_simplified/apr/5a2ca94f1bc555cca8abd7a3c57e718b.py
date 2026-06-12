from math import factorial


def solve(n, p, a):
    if p == 9:
        return 1 if n >= a[9] else 0
    elif p == 0:
        total = 0
        for i in range(a[0], n):
            ways = solve(n - i, 1, a)
            ways *= factorial(n - 1)
            ways //= factorial(i)
            ways //= factorial(n - 1 - i)
            total += ways
        return total
    else:
        total = 0
        for i in range(a[p], n + 1):
            ways = solve(n - i, p + 1, a)
            ways *= factorial(n)
            ways //= factorial(i)
            ways //= factorial(n - i)
            total += ways
        return total


MOD = 1000000007
n = int(input())
a = list(map(int, input().rstrip().split()))
ans = 0
for i in range(1, n + 1):
    ans += solve(i, 0, a)
    ans %= MOD
print(ans)
