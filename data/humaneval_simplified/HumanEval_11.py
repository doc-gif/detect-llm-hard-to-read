from typing import *


def string_xor(a: str, b: str) -> str:
    def xor(i: str, j: str) -> str:
        return "0" if i == j else "1"

    return "".join(xor(x, y) for x, y in zip(a, b))
