from typing import *


def choose_num(x: int, y: int) -> int:
    if x > y:
        return -1
    if y % 2 == 0:
        return y
    if x == y:
        return -1
    return y - 1
