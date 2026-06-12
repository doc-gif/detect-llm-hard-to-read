from typing import *
import math


def prime_fib(n: int):
    def is_prime(p: int) -> bool:
        if p < 2:
            return False
        limit = int(math.sqrt(p)) + 1
        for k in range(2, limit):
            if p % k == 0:
                return False
        return True

    fib = [0, 1]
    while True:
        fib.append(fib[-1] + fib[-2])
        if is_prime(fib[-1]):
            n -= 1
            if n == 0:
                return fib[-1]
