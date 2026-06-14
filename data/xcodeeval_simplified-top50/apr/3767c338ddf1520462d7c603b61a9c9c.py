import itertools as it
from functools import reduce

PRIME = -1
N = 10**9
primes = [PRIME for _ in range(N + 1)]


def factor(n):
    if n == 1:
        return []
    if primes[n] == PRIME:
        return [(n, 1)]
    result = []
    result.append((primes[n], 1))
    n //= primes[n]
    while primes[n] != PRIME:
        if result[-1][0] == primes[n]:
            result[-1] = (primes[n], result[-1][1] + 1)
        else:
            result.append((primes[n], 1))
        n //= primes[n]
    if result[-1][0] == n:
        result[-1] = (n, result[-1][1] + 1)
    else:
        result.append((n, 1))
    return result


def all_divisors(prime_factorization):
    if not prime_factorization:
        return [1]
    factor_with_mult = []
    for prime, exp in prime_factorization:
        powers = [prime**i for i in range(exp + 1)]
        factor_with_mult.append(powers)
    result = []
    for divisor in it.product(*factor_with_mult):
        result.append(reduce(lambda x, y: x * y, divisor))
    return result


if __name__ == "__main__":
    for i in range(2, N + 1):
        if primes[i] == PRIME:
            j = 2
            while j * i < N + 1:
                primes[j * i] = i
                j += 1
    primes[0] = primes[1] = 0
    n = int(input())
    min_result = 10**9
    max_result = 0
    for divisor in all_divisors(factor(n)):
        for div2 in all_divisors(factor(divisor)):
            if div2 * div2 > divisor:
                break
            a = n // divisor + 1
            b = divisor // div2 + 2
            c = div2 + 2
            value = c * b + (a - 1) * 2 * (b + c - 2)
            min_result = min(min_result, value)
            max_result = max(max_result, value)
    print(f"{min_result} {max_result}")
