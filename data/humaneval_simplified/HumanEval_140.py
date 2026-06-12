from typing import *


def fix_spaces(text: str) -> str:
    new_text = ""
    space_start = 0
    i = 0
    while i < len(text):
        if text[i] != " ":
            space_len = i - space_start
            if space_len > 2:
                new_text += "-"
            elif space_len > 0:
                new_text += "_" * space_len
            new_text += text[i]
            space_start = i + 1
        i += 1
    trailing_space_len = len(text) - space_start
    if trailing_space_len > 2:
        new_text += "-"
    elif trailing_space_len > 0:
        new_text += "_"
    return new_text
