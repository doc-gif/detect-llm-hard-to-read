#In the name of Allah

from sys import stdin, stdout
input = stdin.readline

n, a, b, c = map(int, input().split())
dp = [0] + [-float("inf")] * n

for i in range(a, n + 1):
         dp[i] = max(dp[i], dp[i - a] + 1)
         
for i in range(b, n + 1):
         dp[i] = max(dp[i], dp[i - b] + 1)
         
for i in range(c, n + 1):
         dp[i] = max(dp[i], dp[i - c] + 1)

stdout.write(str(dp[n]))
