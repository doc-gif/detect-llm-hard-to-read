import itertools as it
from functools import reduce

PRIME = -1

N = 10**9

primes = [PRIME for x in range(N + 1)]


def factor(n):
    """
    >>> factor(2)
    [(2, 1)]

    >>> factor(6)
    [(3, 1), (2, 1)]

    >>> factor(98)
    [(7, 2), (2, 1)]

    >>> factor(1)
    []
    """
    if n == 1:
        return []
    if primes[n] == PRIME:
        return [(n, 1)]
    result = []
    result += [(primes[n], 1)]
    n //= primes[n]

    while primes[n] != PRIME:
        if result[-1][0] == primes[n]:
            result[-1] = (primes[n], result[-1][1] + 1)
        else:
            result += [(primes[n], 1)]
        n //= primes[n]

    if result[-1][0] == n:
        result[-1] = (n, result[-1][1] + 1)
    else:
        result += [(n, 1)]

    return result


def all_divisors(prime_factorization):
    """
    >>> all_divisors(factor(6))
    [1, 2, 3, 6]

    >>> all_divisors(factor(12))
    [1, 2, 4, 3, 6, 12]

    >>> all_divisors(factor(7))
    [1, 7]

    >>> all_divisors(factor(1))
    [1]
    """
    if len(prime_factorization) == 0:
        return [1]
    result = []
    factor_with_mult = []
    for pfactor in prime_factorization:
        factor_with_mult += [[1]]
        for _ in range(pfactor[1]):
            factor_with_mult[-1] += [factor_with_mult[-1][-1] * pfactor[0]]
    for divisor in it.product(*factor_with_mult):
        result += [reduce(lambda x, y: x * y, divisor)]
    return result


if __name__ == '__main__':
    # sieve
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
            min_result = min([min_result,
                              c * b + (a - 1) * 2 *
                              (b + c - 2)])
            max_result = max([max_result,
                              c * b + (a - 1) * 2 *
                              (b + c - 2)])
    print(str(min_result) + " " + str(max_result))
