def main():
    n, k = read_two_ints()
    low, answer, high = 0, 0, n * k
    while low <= high:
        mid = (low + high) // 2
        if can_make(mid, n, k):
            answer, high = mid, mid - 1
        else:
            low = mid + 1
    print(answer)
def can_make(m, n, k):
    count = 0
    divisor = 1
    while m // divisor != 0:
        count += m // divisor
        divisor *= k
    return count >= n
def read_int():
    return int(input())
def read_two_ints():
    return map(int, input().split())
def read_int_array():
    return list(map(int, input().split()))
from sys import *
import inspect
import re
from math import *
import threading
from collections import *
from pprint import pprint as pp
mod = 998244353
MAX = 10**5
def debug(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r"\bdebug\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)", line)
        print("%s %d" % (m.group(1), p))
def vector(size, val=0):
    return [val for _ in range(size)]
def matrix(rows, cols, val=0):
    return [[val for _ in range(cols)] for _ in range(rows)]
def threaded_main():
    sys.setrecursionlimit(100000000)
    threading.stack_size(40960000)
    thread = threading.Thread(target=main)
    thread.start()
if __name__ == "__main__":
    main()