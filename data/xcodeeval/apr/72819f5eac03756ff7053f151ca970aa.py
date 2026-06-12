#!/usr/bin/env python3

import itertools

PRIME = int(998244353)

def ri(string):
    return list(map(int, string.split(' ')))

def power(a, b):
    if b == 0: return 1
    i = 2
    a_power = [a]
    while i <= b:
        a_power.append(a_power[-1]*a_power[-1] % PRIME)
        i *= 2

    bin_b = list(map(int, bin(b)[:1:-1]))
    # print(a_power, bin_b)
    a_power = itertools.compress(a_power, bin_b)
    # print(a_power)
    res = 1
    for p in a_power:
        # print(res, p)
        res = res * p % PRIME
    return res


n = int(input())

sums = []
sums.append(1)
sums.append(1)
for i in range(2, n+1):
    sums.append(sum(sums[-1::-2]) % PRIME)
    # print(f'{i}: {sums[i]}')

# print(sums)
x = sums[n]
# print(x)
y_inv = power(2, n*(PRIME-2))

print(x*y_inv % PRIME)


# sums = []
# sums.append(1)
# sums.append(1)
#     # print(f'{i}: {sums[i]}')
# for i in range(2, n+1):
#     sums.append(sum(sums[-1::-2]) % PRIME)

