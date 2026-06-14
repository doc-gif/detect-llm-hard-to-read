from typing import *


def int_to_mini_roman(number: int) -> str:
    num = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    sym = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    result = []
    for value, symbol in zip(num, sym):
        count = number // value
        if count:
            result.append(symbol * count)
            number %= value
    return "".join(result).lower()
