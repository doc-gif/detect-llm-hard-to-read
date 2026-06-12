dp = {}
 
def solve(x):
	if x == 0:
		return 0
	if x in dp.keys():
		return dp[x]
	limit = 1
	cnt = 1
	while limit <= x:
		limit = limit * 10 + 1
		cnt += 1
	prv = limit // 10
	c1 = solve(x % prv) + (x // prv) * (cnt - 1)
	c2 = solve((limit-x) % prv) + cnt + (cnt - 1) * ((limit - x) // prv)
	dp[x] = min(c1,c2)
	return min(c1,c2)
 
n = int(input())
print(solve(n))