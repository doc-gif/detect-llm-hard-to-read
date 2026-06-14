from typing import List


def median(l: List[float]) -> float:
    sorted_l = sorted(l)
    mid = len(sorted_l) // 2
    if len(sorted_l) % 2:
        return sorted_l[mid]
    else:
        return (sorted_l[mid - 1] + sorted_l[mid]) / 2.0
