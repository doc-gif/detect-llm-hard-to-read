__author__ = "MoonBall"
import sys
T = 1
MOD = 1000000007
def process():
    P, K = map(int, input().split())
    k = [(K * x) % P for x in range(P)]
    if K == 0:
        print(pow(P, P - 1, MOD))
        return
    visited = [0] * P
    cycle_len_count = [0] * P
    result = 1
    for start in range(P):
        if visited[start]:
            continue
        length = 1
        current = start
        visited[current] = 1
        while not visited[k[current]]:
            current = k[current]
            visited[current] = 1
            length += 1
        cycle_len_count[length] += 1
    for length in range(1, P):
        count = cycle_len_count[length]
        if count == 0:
            continue
        total = length * count + (cycle_len_count[1] if length > 1 else 0)
        result = result * pow(total, count, MOD) % MOD
    print(result)
for _ in range(T):
    process()