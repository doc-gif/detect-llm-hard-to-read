import sys
input = sys.stdin.buffer.readline
sys.setrecursionlimit(10**7)

n, m = [int(item) for item in input().split()]
if n > m:
    n, m = m, n
if n == 1 and m == 1:
    print(2)
    exit()
dp = [[0] * m for _ in range(4)]

dp[0][1] = 1
dp[1][1] = 1
dp[2][1] = 1
dp[3][1] = 1

for i in range(2, m):
    dp[0][i] += dp[2][i-1] 
    dp[1][i] += dp[0][i-1] 
    dp[1][i] += dp[2][i-1] 
    dp[2][i] += dp[1][i-1] 
    dp[2][i] += dp[3][i-1] 
    dp[3][i] += dp[1][i-1] 

# for line in dp:
#     print(line)
lr = 0
ud = 0

for i in range(4):
    lr += dp[i][m-1]
    ud += dp[i][n-1]

if n == 1:
    print(lr)
    exit()
else:
    print(lr + ud - 2)