from typing import *


def words_string(s):
    if not s:
        return []
    return "".join(" " if c == "," else c for c in s).split()
