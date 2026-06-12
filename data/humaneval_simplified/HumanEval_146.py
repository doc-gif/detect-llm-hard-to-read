from typing import *


def specialFilter(nums):
    count = 0
    odd_digits = {1, 3, 5, 7, 9}
    for num in nums:
        if num > 10:
            s = str(num)
            if int(s[0]) in odd_digits and int(s[-1]) in odd_digits:
                count += 1
    return count
