from typing import List
import math


def sum_squares(lst: List[float]) -> int:
    return sum(math.ceil(num) ** 2 for num in lst)
