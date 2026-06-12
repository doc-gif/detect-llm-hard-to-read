import os
import sys
from io import BytesIO, IOBase

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2)
            self.buffer.write(b)
            self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2)
            self.buffer.write(b)
            self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0)
            self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")
from math import ceil


def prod(a, mod=10**9 + 7):
    ans = 1
    for each in a:
        ans = (ans * each) % mod
    return ans


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def lcm(a, b):
    return a * b // gcd(a, b)


def binary(x, length=16):
    y = bin(x)[2:]
    return y if len(y) >= length else "0" * (length - len(y)) + y


for _ in range(int(input()) if not True else 1):
    s = [int(k) if k.isdigit() else k for k in input()]
    start = 0
    if len(s) > 1:
        start = 10 ** (len(s) - 1)
    while start % 25:
        start += 1
    ans = 0
    done = False
    while not done:
        x = start
        ind = len(s) - 1
        XV = None
        pos = True
        while x:
            if ind < 0:
                pos = False
                done = True
                break
            d = x % 10
            if s[ind] == "_":
                pass
            elif s[ind] == "X":
                if XV is None:
                    XV = d
                elif XV != d:
                    pos = False
            else:
                if s[ind] != d:
                    pos = False
            x //= 10
            ind -= 1
        if pos:
            ans += 1
        start += 25
    print(ans)
