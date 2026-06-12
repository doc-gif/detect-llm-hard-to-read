import math
import os
import random
import re
import sys
from itertools import permutations

if __name__ == "__main__":
    a = list(map(int, input().rstrip().split()))
    if a[1] == a[0]:
        print(0)
    if a[0] == 0:
        print(-1)
    elif a[1] % a[0] == 0:
        d = a[1] / a[0]
        k, p = 0, 0
        if d % 2 == 0:
            k, p = 2, 3
        elif d % 3 == 0:
            k, p = 3, 2
        c = 0
        while d % k == 0:
            c += 1
            d /= k
        while d % p == 0:
            c += 1
            d /= p
        print(c)
    else:
        print(-1)
