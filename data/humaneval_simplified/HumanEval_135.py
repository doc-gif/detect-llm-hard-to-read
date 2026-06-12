from typing import List


def can_arrange(arr: List[int]) -> int:
    ind = -1
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            ind = i
    return ind
