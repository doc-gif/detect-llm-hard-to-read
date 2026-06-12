from typing import *


def exchange(lst1: List[int], lst2: List[int]) -> str:
    odd_count = sum(1 for x in lst1 if x % 2 == 1)
    even_count = sum(1 for x in lst2 if x % 2 == 0)
    return "YES" if even_count >= odd_count else "NO"
