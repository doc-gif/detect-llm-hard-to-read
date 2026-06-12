n, m = map(int, input().split())
dp = [0] * (n + 2)
s = [0] * (n + 2)
dp[n] = 1
s[n] = 1
for i in range(n-1, 0, -1):
    dp[i] = s[i+1]
    for j in range(2, n // i + 1):
        # add sum from i*j to i*(j+1) - 1
        # from cells divided by j
        h = min(n + 1, (i + 1) * j)
        dp[i] = (dp[i] + s[i * j] - s[h]) % m
        # print("  i=",i,"j=", j, "h=",h)
    s[i] = (s[i+1] + dp[i]) % m
    # print ("i=", i)
    # print("dp:", * dp)
    # print("s:", *s)
print(dp[1])

