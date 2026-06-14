from typing import *


def fibfib(n: int) -> int:
    if n == 0 or n == 1:
        return 0
    if n == 2:
        return 1
    return fibfib(n - 1) + fibfib(n - 2) + fibfib(n - 3)
