import math
from collections import defaultdict

mp = defaultdict(int)


def primeFactor(a):
    i = 2
    while i * i <= a:
        while a % i == 0:
            mp[i] += 1
            a //= i
        i += 1
    if a > 1:
        mp[a] += 1


def trailingZero(a, n):
    ans = 0
    while n > 0:
        ans += n // a
        n //= a
    return ans

n, b = map(int, input().split())
ans = int(1e50)
primeFactor(b)
for it in mp:
    first = it
    second = mp[it]
    temp = trailingZero(first, n)
    ans = min(ans, temp // second)
print(ans)

