from typing import List


def maximum(arr: List[int], k: int) -> List[int]:
    if k == 0:
        return []
    arr.sort()
    return arr[-k:]
