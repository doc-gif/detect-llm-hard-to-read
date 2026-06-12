from typing import *


def unique_digits(x):
    return sorted(i for i in x if all(int(c) % 2 for c in str(i)))
