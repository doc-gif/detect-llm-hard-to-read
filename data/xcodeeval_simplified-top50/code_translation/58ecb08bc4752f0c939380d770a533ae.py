from math import factorial
dp = [[-1] * 101 for _ in range(101)]
def solve(n, p, a):
    if dp[n][p] != -1:
        return dp[n][p]
    if p == 9:
        dp[n][p] = 1 if n >= a[9] else 0
        return dp[n][p]
    if p == 0:
        ans = 0
        for i in range(a[0], n):
            z = solve(n - i, 1, a)
            z *= factorial(n - 1)
            z //= factorial(i)
            z //= factorial(n - 1 - i)
            ans += z
        dp[n][p] = ans
        return ans
    ans = 0
    for i in range(a[p], n + 1):
        z = solve(n - i, p + 1, a)
        z *= factorial(n)
        z //= factorial(i)
        z //= factorial(n - i)
        ans += z
    dp[n][p] = ans
    return ans
MOD = 1000000007
n = int(input())
a = list(map(int, input().split()))
ans = 0
for i in range(1, n + 1):
    ans += solve(i, 0, a)
    ans %= MOD
print(ans)