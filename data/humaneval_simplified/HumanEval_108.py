from typing import List


def count_nums(arr: List[int]) -> int:
    def digits_sum(n: int) -> int:
        sign = -1 if n < 0 else 1
        digits = [int(d) for d in str(abs(n))]
        digits[0] *= sign
        return sum(digits)

    return sum(1 for num in arr if digits_sum(num) > 0)
