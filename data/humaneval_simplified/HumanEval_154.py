from typing import *


def cycpattern_check(a: str, b: str) -> bool:
    double_b = b + b
    for start in range(len(a) - len(b) + 1):
        substring = a[start : start + len(b)]
        if any(substring == double_b[i : i + len(b)] for i in range(len(b) + 1)):
            return True
    return False
