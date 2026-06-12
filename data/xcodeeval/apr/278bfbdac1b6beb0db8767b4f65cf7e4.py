#!/usr/bin/env pypy
from __future__ import division, print_function

import os
import sys
from __builtin__ import xrange as range
from cStringIO import StringIO
from future_builtins import ascii, filter, hex, map, oct, zip
from io import IOBase

import __pypy__


def memoize(f):
    """ Memoization decorator for a function taking one or more arguments. """

    class memodict(dict):
        def __getitem__(self, *key):
            return dict.__getitem__(self, key)

        def __missing__(self, key):
            ret = self[key] = f(*key)
            return ret

    return memodict().__getitem__


def main():
    n, T = map(int, input().split())
    t, g = [0] * n, [0] * n
    for i in range(n):
        t[i], g[i] = map(int, input().split())

    def solve(T, p, mask):
        if T < 0:
            return 0
        if T == 0:
            return 1

        res = 0
        for i in range(n):
            if mask[i] == 0 and p != g[i]:
                new_mask = mask[:]
                new_mask[i] = 1
                res += solve(T - t[i], g[i], new_mask)

        return res

    print(solve(T, -1, [0] * n))


# region fastio

BUFSIZE = 8192


class FastI(IOBase):
    def __init__(self, file):
        self._fd = file.fileno()
        self._buffer = StringIO()
        self.newlines = 0

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count("\n") + (not b)
            ptr = self._buffer.tell()
            self._buffer.seek(0, 2), self._buffer.write(b), self._buffer.seek(ptr)
        self.newlines -= 1
        return self._buffer.readline()


class FastO(IOBase):
    def __init__(self, file):
        self._fd = file.fileno()
        self._buffer = __pypy__.builders.StringBuilder()
        self.write = lambda s: self._buffer.append(s)

    def flush(self):
        os.write(self._fd, self._buffer.build())
        self._buffer = __pypy__.builders.StringBuilder()


def print(*args, **kwargs):
    sep, file = kwargs.pop("sep", " "), kwargs.pop("file", sys.stdout)
    at_start = True
    for x in args:
        if not at_start:
            file.write(sep)
        file.write(str(x))
        at_start = False
    file.write(kwargs.pop("end", "\n"))
    if kwargs.pop("flush", False):
        file.flush()


sys.stdin, sys.stdout = FastI(sys.stdin), FastO(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# endregion

if __name__ == "__main__":
    main()
