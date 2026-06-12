from typing import List
import math


def factorize(n: int) -> List[int]:
    factors = []
    divisor = 2
    limit = int(math.isqrt(n)) + 1
    while divisor <= limit:
        if n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        else:
            divisor += 1
    if n > 1:
        factors.append(n)
    return factors
