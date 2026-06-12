from math import *
import sys

dp = {}
for i in range(102):
    for j in range(-101, 102):
        for k in range(102):
            dp[(i, j, k)] = None


def rec(i, parity, m, a):
    if m < 0:
        return -10000000
    if dp[(i, parity, m)] is not None:
        return dp[(i, parity, m)]
    parity += -1 if a[i] % 2 == 0 else 1
    if i == len(a) - 1:
        if parity == 0:
            return 0
        else:
            return -1000000
    best = rec(i + 1, parity, m, a)
    if parity == 0:
        best = max(best, 1 + rec(i + 1, 0, m - abs(a[i] - a[i + 1]), a))
    dp[(i, parity, m)] = best
    return best


def main():
    n, money = [int(x) for x in input().split(" ")]
    a = [int(x) for x in input().split(" ")]
    ans = rec(1, a[0] % 2, money, a)
    print(ans)


if __name__ == "__main__":
    main()
