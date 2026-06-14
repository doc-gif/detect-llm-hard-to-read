from typing import *


def minSubArraySum(nums: List[int]) -> int:
    max_negated_sum = 0
    current_negated_sum = 0
    for num in nums:
        current_negated_sum += -num
        if current_negated_sum < 0:
            current_negated_sum = 0
        max_negated_sum = max(max_negated_sum, current_negated_sum)
    if max_negated_sum == 0:
        max_negated_sum = max(-num for num in nums)
    return -max_negated_sum
