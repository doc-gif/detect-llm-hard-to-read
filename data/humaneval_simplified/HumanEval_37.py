from typing import *


def sort_even(l: list):
    evens = l[::2]
    odds = l[1::2]
    evens.sort()
    result = []
    for even_val, odd_val in zip(evens, odds):
        result.extend([even_val, odd_val])
    if len(evens) > len(odds):
        result.append(evens[-1])
    return result
