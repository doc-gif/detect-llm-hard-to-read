from typing import *


def intersection(interval1: List[int], interval2: List[int]) -> str:
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n == 2:
            return True
        for i in range(2, n):
            if n % i == 0:
                return False
        return True

    left = max(interval1[0], interval2[0])
    right = min(interval1[1], interval2[1])
    length = right - left
    if length > 0 and is_prime(length):
        return "YES"
    return "NO"
