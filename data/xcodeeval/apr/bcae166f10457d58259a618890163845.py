#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Codeforces Round #554 (Div. 2)

Problem C. Neko does Maths

:author:         Kitchen Tong
:mail:    kctong529@gmail.com

Please feel free to contact me if you have any question
regarding the implementation below.
"""

__version__ = '1.0'
__date__ = '2019-04-24'

import sys


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def prime_sieve(size):
    sieve = [0, 0] + [1] * (size - 1)
    primes = []
    for i in range(2, size+1):
        if sieve[i] == 1:
            for j in range(i**2, size+1, i):
                sieve[j] = 0
            primes.append(i)
    return (sieve, primes)

def memoize(func):
    memo = {}

    def wrapper(*args):
        n, p, s = args
        if n not in memo:
            memo[n] = func(n, p, s)
        return memo[n]
    return wrapper

@memoize
def rec_fact(n, primes, sieve):
    if sieve[n] == 1:
        return [n]
    if n == 1:
        return []
    for p in primes:
        if n % p == 0:
            return [p] + rec_fact(n//p, primes, sieve)
    return -1

def factorize(n, primes, sieve):
    if sieve[n] == 1:
        return [n]
    p_factors = rec_fact(n, primes, sieve)
    p_dict = dict()
    for p in p_factors:
        if p not in p_dict:
            p_dict[p] = 1
        else:
            p_dict[p] += 1
    factors = [1]
    for p, k in p_dict.items():
        for f in list(factors):
            for exp in range(1, k+1):
                factors += [f * (p ** exp)]
    return sorted(factors)

def solve(a, b):
    a, b = min(a, b), max(a, b)
    if b % a == 0:
        return 0
    diff = b - a
    sieve, primes = prime_sieve(diff)
    factors = factorize(diff, primes, sieve)
    k, lcm = 0, a * b
    for f in factors:
        step = a % f
        if step > 0:
            step = f - step
        this_lcm = (a + step) * (b + step) // gcd(a+step, b+step)
        if this_lcm < lcm:
            lcm = this_lcm
            k = step
    return k

def main(argv=None):
    a, b = map(int, input().split())
    print(solve(a, b))
    return 0

if __name__ == "__main__":
    STATUS = main()
    sys.exit(STATUS)

