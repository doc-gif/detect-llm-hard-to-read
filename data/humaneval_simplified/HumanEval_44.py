from typing import *


def change_base(x: int, base: int) -> str:
    digits = []
    while x > 0:
        digits.append(str(x % base))
        x //= base
    return "".join(reversed(digits))
