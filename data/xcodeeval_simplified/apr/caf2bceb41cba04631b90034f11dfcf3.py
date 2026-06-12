import sys

input = sys.stdin.readline
n, m = map(int, input().split())
S = list(range(n + 1))
for i in range(2, n + 1):
    if S[i] == i:
        for j in range(i, n + 1, i):
            if S[j] == j:
                S[j] = i


def get_divisors(x):
    prime_factors = []
    while x != 1:
        prime_factors.append(S[x])
        x //= S[x]
    divisors = {1}
    for p in prime_factors:
        divisors |= {d * p for d in divisors}
    return divisors


DP = [0] * (n + 1)
DP[1] = 1
DP[2] = 2
DP[3] = 5
for i in range(4, n + 1):
    total = DP[i - 1] * 2 + 1
    for d in get_divisors(i):
        if d == 1 or d == i:
            continue
        total += DP[i // d] - DP[(i - 1) // d]
    DP[i] = total % m
print(DP[n])
