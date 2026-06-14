from typing import *


def vowels_count(s: str) -> int:
    vowels = "aeiouAEIOU"
    count = sum(1 for char in s if char in vowels)
    if s[-1] in ("y", "Y"):
        count += 1
    return count
