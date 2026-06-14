from typing import *


def sort_even(l: list):
    evens = sorted(l[::2])
    odds = l[1::2]
    result = []
    for e, o in zip(evens, odds):
        result.extend([e, o])
    if len(evens) > len(odds):
        result.append(evens[-1])
    return result
