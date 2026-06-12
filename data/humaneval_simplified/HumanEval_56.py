from typing import *


def correct_bracketing(brackets: str) -> bool:
    depth = 0
    for b in brackets:
        depth += 1 if b == "<" else -1
        if depth < 0:
            return False
    return depth == 0
