from collections import Counter
def primes(n):
    factor_counts = Counter()
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factor_counts[divisor] += 1
            n //= divisor
        divisor += 1
    if n > 1:
        factor_counts[n] += 1
    return list(factor_counts.values())
def run():
    number = int(input())
    exponents = primes(number)
    result = 1
    for exp in exponents:
        result *= exp + 1
    print(result)
if __name__ == "__main__":
    run()