from typing import *


def vowels_count(s: str) -> int:
    vowels = "aeiouAEIOU"
    count = sum(1 for c in s if c in vowels)
    if s[-1] in ("y", "Y"):
        count += 1
    return count
