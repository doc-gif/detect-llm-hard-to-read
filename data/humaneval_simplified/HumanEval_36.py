from typing import *


def fizz_buzz(n: int):
    ns = [i for i in range(n) if i % 11 == 0 or i % 13 == 0]
    s = "".join(map(str, ns))
    return sum(1 for c in s if c == "7")
