from typing import *


def minSubArraySum(nums: List[int]) -> int:
    max_neg_sum = 0
    current_sum = 0
    for num in nums:
        current_sum += -num
        if current_sum < 0:
            current_sum = 0
        max_neg_sum = max(current_sum, max_neg_sum)
    if max_neg_sum == 0:
        max_neg_sum = max(-num for num in nums)
    return -max_neg_sum
