from typing import *


def split_words(txt: str) -> Union[List[str], int]:
    if " " in txt:
        return txt.split()
    if "," in txt:
        return txt.replace(",", " ").split()
    return len([c for c in txt if c.islower() and ord(c) % 2 == 0])
