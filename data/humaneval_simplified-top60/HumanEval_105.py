from typing import *


def by_length(arr: List[int]) -> List[str]:
    number_names = {
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine",
    }
    return [
        number_names[num] for num in sorted(arr, reverse=True) if num in number_names
    ]
