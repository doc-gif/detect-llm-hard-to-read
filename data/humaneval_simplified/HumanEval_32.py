from typing import List
import math


def poly(coefficients: List[float], x: float) -> float:
    return sum(coeff * (x**i) for i, coeff in enumerate(coefficients))


def find_zero(coefficients: List[float]) -> float:
    left, right = -1.0, 1.0
    while poly(coefficients, left) * poly(coefficients, right) > 0:
        left *= 2.0
        right *= 2.0
    while right - left > 1e-10:
        mid = (left + right) / 2.0
        if poly(coefficients, mid) * poly(coefficients, left) > 0:
            left = mid
        else:
            right = mid
    return left
