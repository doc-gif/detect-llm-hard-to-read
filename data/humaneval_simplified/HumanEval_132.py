from typing import *


def is_nested(string: str) -> bool:
    opening = [i for i, ch in enumerate(string) if ch == "["]
    closing = [i for i, ch in enumerate(string) if ch == "]"][::-1]
    cnt = 0
    j = 0
    for idx in opening:
        if j < len(closing) and idx < closing[j]:
            cnt += 1
            j += 1
    return cnt >= 2
