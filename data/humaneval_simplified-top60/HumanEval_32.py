from typing import List
import math


def poly(coeffs: List[float], x: float) -> float:
    return sum(coeff * math.pow(x, i) for i, coeff in enumerate(coeffs))


def find_zero(coeffs: List[float]) -> float:
    left, right = -1.0, 1.0
    while poly(coeffs, left) * poly(coeffs, right) > 0:
        left *= 2.0
        right *= 2.0
    while right - left > 1e-10:
        mid = (left + right) / 2.0
        if poly(coeffs, mid) * poly(coeffs, left) > 0:
            left = mid
        else:
            right = mid
    return left
