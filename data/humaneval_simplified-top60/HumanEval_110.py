from typing import *


def exchange(lst1: List[int], lst2: List[int]) -> str:
    odd_in_lst1 = sum(1 for x in lst1 if x % 2 == 1)
    even_in_lst2 = sum(1 for y in lst2 if y % 2 == 0)
    return "YES" if even_in_lst2 >= odd_in_lst1 else "NO"
