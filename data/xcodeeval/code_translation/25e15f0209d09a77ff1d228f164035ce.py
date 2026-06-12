import math
n = int(input())
nums = input().split()
for i in range(n):
    nums[i] = int(nums[i])
nums.sort()
if (nums[n-1] > 25):
    print(nums[n-1] - 25)
else:
    print(0)




