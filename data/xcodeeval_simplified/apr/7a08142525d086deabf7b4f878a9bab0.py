import sys
import math
import collections

M = 10**9 + 7


def solve():
    n, k = map(int, input().split())
    factor = 2**k
    ans = 1
    for i in range(n):
        ans = (ans * factor) % M
    return (ans * 2) % M


test = int(input())
count1 = 1
while count1 <= test:
    ans = solve()
    sys.stdout.write(str(ans) + "\n")
    count1 += 1
