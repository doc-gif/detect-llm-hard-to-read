import math
n = int(input())
nums = [int(x) for x in input().split()[:n]]
nums.sort()
max_num = nums[-1]
print(max_num - 25 if max_num > 25 else 0)