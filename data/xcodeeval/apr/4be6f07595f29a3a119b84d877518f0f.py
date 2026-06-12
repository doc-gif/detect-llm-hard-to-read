#----------------------------IMPORTING LIBRARIES----------------------------#
import gc
import math
from math import log2
import heapq
from math import floor, ceil
from collections import deque
from posixpath import curdir
from re import L
import sys
from collections import Counter
#----------------------------LAMBDAS AND DEFAULT----------------------------#
I = lambda:list(map(int,input().split()))
MAP = lambda:map(int, input().split())
input = sys.stdin.readline
sys.setrecursionlimit(10000)

MOD = 998244353
#-----------------------------STANDARD FUNCTIONS----------------------------#
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)

def isSubsequence(s, t):
    for i in range (0, len(s)):    
        try:
            index = t.index(s[i])
        except ValueError: 
            return False
        t = t[index+1:]
    return True

def bisect_right(a, x):
        lo, hi = 0, len(a)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if a[mid] > x: hi = mid
            else: lo = mid + 1
        return lo
    
def bisect_left(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if a[mid] < x: lo = mid + 1
        else: hi = mid
    return lo

def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        pivot = left + (right - left) // 2
        if nums[pivot] == target:
            return pivot
        if target < nums[pivot]:
            right = pivot - 1
        else:
            left = pivot + 1
    return -1

#------------------------------HELPER FUNCTION------------------------------#
def prefixSum(arr):
    dp = [arr[0]]
    arrLen = len(arr)
    for i in range(1, arrLen): dp.append(dp[-1] + arr[i])
    return dp

def suffixSum(arr):
    arrLen = len(arr)
    dp = [0] * arrLen
    dp[-1] = arr[-1]
    for i in range(arrLen-2, -1, -1): dp[i] = dp[i+1] + arr[i]
    return dp

def fun():
    return 

MAX = 10**6 + 2

def solve():
    N = int(input())
    if N == 1:
        print(1)
    elif N == 2:
        print(2)
    else:
        print(2**N-1)

    

    


    
#---------------------------------DRIVER CODE--------------------------------#
TC = int(input())
#TC = 1
for testcases in range(TC):
    solve()