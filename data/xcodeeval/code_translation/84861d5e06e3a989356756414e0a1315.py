prime = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
dp = [[10**18 for i in range(15)] for j in range(1006)]
inf = 10**18
for pw in range(64):
	dp[pw + 1][0] = 2**pw
for idx in range(1,13):
	for i in range(1005):
		for pw in range(64):
			if(i % (pw + 1)==0):
				if(dp[i // (pw + 1)][idx-1] > inf // (prime[idx]**pw)):break
				dp[i][idx] = min(dp[i][idx],dp[i // (pw + 1)][idx-1] *(prime[idx]**pw))
print(dp[int(input())][12])