import sys


def input():
    return sys.stdin.readline().strip()


n, mod = map(int, input().split())
FACT_LIMIT = 500


def mod_pow(base, exp):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result


def mod_inv(x):
    return mod_pow(x, mod - 2)


factorials = [1]
current = 1
for i in range(1, FACT_LIMIT):
    current = (current * i) % mod
    factorials.append(current)
inv_factorials = [0] * (FACT_LIMIT - 1) + [mod_inv(factorials[FACT_LIMIT - 1])]
for i in range(FACT_LIMIT - 2, -1, -1):
    inv_factorials[i] = inv_factorials[i + 1] * (i + 1) % mod


def comb(x, y):
    if y < 0 or y > x:
        return 0
    if x > FACT_LIMIT:
        y = min(y, x - y)
        numerator = 1
        for i in range(x, x - y, -1):
            numerator = (numerator * i) % mod
        return (numerator * inv_factorials[y]) % mod
    else:
        result = factorials[x]
        result = (result * inv_factorials[y]) % mod
        return (result * inv_factorials[x - y]) % mod


powers_of_two = [1]
for _ in range(n + 10):
    powers_of_two.append((powers_of_two[-1] * 2) % mod)
comb_table = [[0] * (n + 10) for _ in range(n + 10)]
for i in range(n + 10):
    for j in range(n + 10):
        comb_table[i][j] = comb(i, j)
dp = [[0] * (n + 1) for _ in range(n + 2)]
dp[0][0] = 1
for i in range(n + 2):
    for j in range(n + 1):
        for k in range(1, n + 1):
            next_i = i + k + 1
            next_j = j + k
            if next_i <= n + 1 and next_j <= n:
                dp[next_i][next_j] += (
                    dp[i][j] * comb_table[j + k][k] * powers_of_two[k - 1]
                )
                dp[next_i][next_j] %= mod
            if next_j == n:
                break
        if next_i == n + 1:
            break
print(sum(dp[-1]) % mod)
