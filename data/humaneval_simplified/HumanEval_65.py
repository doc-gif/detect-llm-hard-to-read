from typing import *


def circular_shift(x: int, shift: int) -> str:
    s = str(x)
    if shift > len(s):
        return s[::-1]
    return s[-shift:] + s[:-shift]
