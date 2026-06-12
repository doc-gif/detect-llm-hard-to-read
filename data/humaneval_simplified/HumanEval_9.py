from typing import List


def rolling_max(numbers: List[int]) -> List[int]:
    result = []
    running_max = None
    for n in numbers:
        running_max = n if running_max is None else max(running_max, n)
        result.append(running_max)
    return result
