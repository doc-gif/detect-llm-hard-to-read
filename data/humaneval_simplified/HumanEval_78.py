from typing import *


def hex_key(num: str) -> int:
    primes = {"2", "3", "5", "7", "B", "D"}
    return sum(1 for ch in num if ch in primes)
