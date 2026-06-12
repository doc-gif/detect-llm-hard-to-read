import sys

input = sys.stdin.readline
MOD = 10**9 + 7
MAX = 2 * 10**5
n, k = map(int, input().split())
fact = [1]
for i in range(1, MAX + 1):
    fact.append(fact[-1] * i % MOD)
fact_inv = [pow(fact[-1], MOD - 2, MOD)]
for i in range(MAX, 0, -1):
    fact_inv.append(fact_inv[-1] * i % MOD)
fact_inv.reverse()


def comb(a, b):
    if 0 <= b <= a:
        return fact[a] * fact_inv[b] * fact_inv[a - b] % MOD
    return 0


dp = [0] * (n + 1)
dp[0] = 1
for _ in range(n):
    ndp = [0] * (n + 1)
    for i in range(n + 1):
        for j in range(max(1, i), n + 1):
            plus = pow(k, i, MOD) * comb(n - i, j - i) * pow(k - 1, n - j, MOD)
            if i == j:
                plus -= pow(k - 1, n, MOD)
            ndp[j] = (ndp[j] + dp[i] * plus) % MOD
    dp = ndp
print(dp[-1])
