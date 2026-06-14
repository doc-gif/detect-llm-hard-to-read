from typing import *


def digits(n: int) -> int:
    product = 1
    odd_count = 0
    for digit_char in str(n):
        digit = int(digit_char)
        if digit % 2 == 1:
            product *= digit
            odd_count += 1
    return 0 if odd_count == 0 else product
