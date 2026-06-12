#!/usr/bin/env python
"""
This file is part of https://github.com/Cheran-Senthil/PyRival.

Copyright 2018 Cheran Senthilkumar all rights reserved,
Cheran Senthilkumar <hello@cheran.io>
Permission to use, modify, and distribute this software is given under the
terms of the MIT License.

"""
from __future__ import division, print_function

import cmath
import itertools
import math
import operator as op
# import random
import sys
from atexit import register
from bisect import bisect_left, bisect_right
# from collections import Counter, MutableSequence, defaultdict, deque
# from copy import deepcopy
# from decimal import Decimal
# from difflib import SequenceMatcher
# from fractions import Fraction
# from heapq import heappop, heappush

if sys.version_info[0] < 3:
    # from cPickle import dumps
    from io import BytesIO as stream
    # from Queue import PriorityQueue, Queue
else:
    # from functools import reduce
    from io import StringIO as stream
    # from pickle import dumps
    # from queue import PriorityQueue, Queue


if sys.version_info[0] < 3:
    class dict(dict):
        """dict() -> new empty dictionary"""
        def items(self):
            """D.items() -> a set-like object providing a view on D's items"""
            return dict.iteritems(self)

        def keys(self):
            """D.keys() -> a set-like object providing a view on D's keys"""
            return dict.iterkeys(self)

        def values(self):
            """D.values() -> an object providing a view on D's values"""
            return dict.itervalues(self)

    input = raw_input
    range = xrange

    filter = itertools.ifilter
    map = itertools.imap
    zip = itertools.izip


def sync_with_stdio(sync=True):
    """Set whether the standard Python streams are allowed to buffer their I/O.

    Args:
        sync (bool, optional): The new synchronization setting.

    """
    global input, flush

    if sync:
        flush = sys.stdout.flush
    else:
        sys.stdin = stream(sys.stdin.read())
        input = lambda: sys.stdin.readline().rstrip('\r\n')

        sys.stdout = stream()
        register(lambda: sys.__stdout__.write(sys.stdout.getvalue()))


def gcd(x, y):
    """greatest common divisor of x and y"""
    while y:
        x, y = y, x % y
    return x


def ntt(a, invert=False):
    j = 0
    for i in range(1, len(a)):
        bit = len(a) >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit

        if i < j:
            a[i], a[j] = a[j], a[i]

    length, cnt = 2, 1
    while length <= len(a):
        wlen = pow(3, 998244353 - 1 - (998244353 - 1 >> cnt) if invert else 998244353 - 1 >> cnt, 998244353)

        for i in range(0, len(a), length):
            w = 1
            for j in range(i, i + length // 2):
                u = a[j]
                v = (a[j + length//2] * w) % 998244353

                a[j] = u + v if u + v < 998244353 else u + v - 998244353
                a[j + length//2] = u - v if u - v >= 0 else u - v + 998244353

                w = (w * wlen) % 998244353

        cnt += 1
        length <<= 1

    if invert:
        n_1 = pow(len(a), 998244351, 998244353)
        for i in range(len(a)):
            a[i] = (a[i] * n_1) % 998244353


def main():
    n, _ = map(int, input().split(' '))

    d = [0] * 1048576
    for i in map(int, input().split(' ')):
        d[i] = 1

    ntt(d)
    d = list(map(lambda x: pow(x, n//2, 998244353), d))
    ntt(d, True)

    print(sum(i*i for i in d) % 998244353)


if __name__ == '__main__':
    sync_with_stdio(False)
    main()
