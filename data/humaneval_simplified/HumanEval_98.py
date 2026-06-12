from typing import *


def count_upper(s: str) -> int:
    return sum(1 for i in range(0, len(s), 2) if s[i] in "AEIOU")
