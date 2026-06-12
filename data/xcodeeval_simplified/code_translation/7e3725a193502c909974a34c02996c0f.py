import math
n = int(input())
factors = []
value = n
for divisor in range(2, n + 1):
    if value % divisor == 0:
        exponent = 0
        while value % divisor == 0:
            exponent += 1
            value //= divisor
        factors.append([divisor, exponent])
product = 1
max_exp_two = 0
for factor, exponent in factors:
    product *= factor
    power_two = int(math.log2(exponent))
    if exponent > (1 << power_two):
        power_two += 1
    max_exp_two = max(max_exp_two, power_two)
needs_adjustment = 0
for factor, exponent in factors:
    if exponent < (1 << max_exp_two):
        needs_adjustment = 1
print(product, max_exp_two + needs_adjustment)