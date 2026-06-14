from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    for i, x in enumerate(numbers):
        for j, y in enumerate(numbers):
            if i != j and abs(x - y) < threshold:
                return True
    return False
