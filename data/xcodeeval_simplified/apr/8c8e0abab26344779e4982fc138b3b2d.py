from collections import *
import sys


def read_int():
    return int(input())


def read_list():
    return list(map(int, input().split()))


test_cases = read_int()
for _ in range(test_cases):
    n, k, l = read_list()
    depths = read_list()
    pattern = list(range(k + 1)) + list(range(k))[::-1]

    def depth_at_time(time, index):
        return depths[index] + pattern[time % (2 * k)]

    def can_win_from(time, index):
        if index == n:
            return True
        if depth_at_time(time, index) > l:
            return False
        for wait in range(2 * k):
            if depth_at_time(time + wait, index) > l:
                break
            if can_win_from(time + wait + 1, index + 1):
                return True
        return False

    for start in range(2 * k):
        if can_win_from(start, 0):
            print("Yes")
            break
    else:
        print("No")
