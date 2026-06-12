from __future__ import division, print_function
import os
import sys
from __builtin__ import xrange as range
from collections import deque
from cStringIO import StringIO
from future_builtins import ascii, filter, hex, map, oct, zip
from io import IOBase
import __pypy__


def process(grid, window_size, rows, cols):
    aux = [[0] * 3000 for _ in range(3000)]
    for i in range(rows):
        window = deque()
        for j in range(window_size):
            while window and grid[i][j] < window[-1]:
                window.pop()
            window.append(grid[i][j])
        aux[0][i] = window[0]
        for j in range(window_size, cols):
            if window[0] == grid[i][j - window_size]:
                window.popleft()
            while window and grid[i][j] < window[-1]:
                window.pop()
            window.append(grid[i][j])
            aux[j - window_size + 1][i] = window[0]
    return aux


def main():
    n, m, a, b = map(int, input().split())
    g, x, y, z = map(float, input().split())
    MOD = int(z)
    MODF = z
    MAGIC = 6755399441055744.0
    SHRT = 65536.0
    MODF_INV = 1.0 / MODF
    SHRT_INV = 1.0 / SHRT
    fround = lambda x: (x + MAGIC) - MAGIC
    fmod = lambda val: val - MODF * fround(MODF_INV * val)
    fmul = lambda a, b, c=0.0: fmod(
        fmod(a * SHRT) * fround(SHRT_INV * b)
        + a * (b - SHRT * fround(b * SHRT_INV))
        + c
    )
    grid = [[0.0] * 3000 for _ in range(3000)]
    for i in range(n):
        for j in range(m):
            grid[i][j] = int(g) % MOD
            g = fmul(g, x, y)
    aux1 = process(grid, b, n, m)
    aux2 = process(aux1, a, m - b + 1, n)
    ans = 0
    for i in range(n - a + 1):
        ans += sum(aux2[i][: m - b + 1])
    print(ans)


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
            ptr = self._buffer.tell()
            self._buffer.seek(0, 2), self._buffer.write(b), self._buffer.seek(ptr)
        self.newlines = 0
        return self._buffer.read()

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
if __name__ == "__main__":
    main()
