import itertools

PRIME = 998244353


def ri(string):
    return list(map(int, string.split()))


def power(a, b):
    if b == 0:
        return 1
    i = 2
    a_power = [a]
    while i <= b:
        a_power.append(a_power[-1] * a_power[-1] % PRIME)
        i *= 2
    bin_b = list(map(int, bin(b)[:1:-1]))
    a_power = itertools.compress(a_power, bin_b)
    res = 1
    for p in a_power:
        res = res * p % PRIME
    return res


n = int(input())
sums = [1, 1]
for i in range(2, n + 1):
    sums.append(sum(sums[-1::-2]) % PRIME)
x = sums[n]
y_inv = power(2, n * (PRIME - 2))
print(x * y_inv % PRIME)
