from typing import *


def fix_spaces(text: str) -> str:
    new_text = ""
    consecutive_spaces = 0
    for char in text:
        if char == " ":
            consecutive_spaces += 1
        else:
            if consecutive_spaces > 2:
                new_text += "-" + char
            elif consecutive_spaces > 0:
                new_text += "_" * consecutive_spaces + char
            else:
                new_text += char
            consecutive_spaces = 0
    if consecutive_spaces > 2:
        new_text += "-"
    elif consecutive_spaces > 0:
        new_text += "_"
    return new_text
