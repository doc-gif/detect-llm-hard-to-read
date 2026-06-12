from typing import *
import re


def is_bored(S: str) -> int:
    sentences = re.split(r"[.?!]\s*", S)
    return sum(sentence.startswith("I ") for sentence in sentences)
