from typing import Tuple


def even_odd_count(num: int) -> Tuple[int, int]:
    even_count = sum(1 for d in str(abs(num)) if int(d) % 2 == 0)
    odd_count = len(str(abs(num))) - even_count
    return (even_count, odd_count)
