n = int(input())
if n == 1:
    print(499122177)
    exit()
if n == 2:
    print(748683265)
    exit()
modulo = 998244353
dp = [0] * (n + 1)
dp[0], dp[1], dp[2] = 1, 1, 1
dp[3] = 2
count1, count2 = dp[1] + dp[3], dp[0] + dp[2]
for i in range(4, n + 1):
    if i % 2 == 0:
        dp[i] = count1
        count2 += dp[i]
        count2 %= modulo
    else:
        dp[i] = count2
        count1 += dp[i]
        count1 %= modulo
y = 1
for _ in range(n):
    y = (y * 2) % modulo
time = 1
yre = 0
while True:
    al = modulo * time + 1
    if al % y == 0:
        yre = al // y
        break
    time += 1
res = (dp[n] * yre) % modulo
print(res)
