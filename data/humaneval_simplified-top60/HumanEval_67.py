from typing import *


def fruit_distribution(s: str, n: int) -> int:
    return n - sum(int(word) for word in s.split() if word.isdigit())
