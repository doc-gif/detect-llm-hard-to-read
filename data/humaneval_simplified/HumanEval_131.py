from typing import *


def digits(n: int) -> int:
    product = 1
    odd_count = 0
    for digit in str(n):
        d = int(digit)
        if d % 2:
            product *= d
            odd_count += 1
    return 0 if odd_count == 0 else product
