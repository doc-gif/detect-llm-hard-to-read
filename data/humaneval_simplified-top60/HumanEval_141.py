from typing import *


def file_name_check(file_name: str) -> str:
    valid_suffixes = {"txt", "exe", "dll"}
    if file_name.count(".") != 1:
        return "No"
    name_part, suffix = file_name.split(".")
    if suffix not in valid_suffixes:
        return "No"
    if not name_part or not name_part[0].isalpha():
        return "No"
    digit_count = sum(1 for char in name_part if char.isdigit())
    if digit_count > 3:
        return "No"
    return "Yes"
