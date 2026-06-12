import math


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def lcm(x, y):
    return (x * y) // gcd(x, y)


a, b = map(int, input().split())
if a > b:
    a, b = b, a
n = b - a
divisors = [1, n]
for i in range(2, int(math.sqrt(n)) + 1):
    if n % i == 0:
        if i * i != n:
            divisors.append(i)
            divisors.append(n // i)
        else:
            divisors.append(i)
k_values = []
lcm_values = []
for divisor in divisors:
    for j in range(1, divisor + 1):
        if (j + b) % divisor == 0:
            k_values.append(j)
            lcm_values.append(lcm(a + j, b + j))
            break
min_lcm = min(lcm_values)
if lcm(a, b) <= min_lcm:
    print(0)
else:
    idx = lcm_values.index(min_lcm)
    print(k_values[idx])
