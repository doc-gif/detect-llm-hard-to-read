import sys
import math
MOD = 998244353
input = sys.stdin.readline
fibo = [1, 1]
for _ in range(200002):
    fibo.append((fibo[-1] + fibo[-2]) % MOD)
n = int(input())
denominator = 1 << n
inv_denominator = pow(denominator, MOD - 2, MOD)
ans = (fibo[n - 1] * inv_denominator) % MOD
print(ans)