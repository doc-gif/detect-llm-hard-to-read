import math
from collections import defaultdict
prime_factor_counts = defaultdict(int)
def compute_prime_factors(number):
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            prime_factor_counts[divisor] += 1
            number //= divisor
        divisor += 1
    if number > 1:
        prime_factor_counts[number] += 1
def count_factor_in_factorial(factor, factorial_base):
    count = 0
    while factorial_base > 0:
        count += factorial_base // factor
        factorial_base //= factor
    return count
n, b = map(int, input().split())
result = int(1e50)
compute_prime_factors(b)
for prime, exponent in prime_factor_counts.items():
    factor_count = count_factor_in_factorial(prime, n)
    result = min(result, factor_count // exponent)
print(result)