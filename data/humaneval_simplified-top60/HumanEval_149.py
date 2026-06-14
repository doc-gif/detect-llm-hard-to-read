from typing import List


def sorted_list_sum(lst: List[str]) -> List[str]:
    lst.sort()
    even_length_strings = [s for s in lst if len(s) % 2 == 0]
    return sorted(even_length_strings, key=len)
