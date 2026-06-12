from __future__ import division, print_function

import os
import sys
from io import BytesIO, IOBase
from math import factorial as fact

def main():
    def isGood(number):
        while number > 0:
            lastDigit = number % 10
            if lastDigit != a and lastDigit != b:
                return False

            number //= 10

        return True

    a, b, n = [ int(x) for x in input().split() ]
    mod = 1000000007

    numOfExcellent = 0

    for numOfA in range(n+1):
        numOfB = n - numOfA
        total = numOfA*a + numOfB*b

        if isGood(total):
            numOfExcellent += (fact(n) // (fact(numOfA) * fact(numOfB))) % mod
            numOfExcellent %= mod

    print(numOfExcellent)


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
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)

class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")

input = lambda: sys.stdin.readline().rstrip("\r\n")

def print(*args, **kwargs):
    """Prints the values to a stream, or to sys.stdout by default."""
    sep = kwargs.pop("sep", " ")
    file = kwargs.pop("file", sys.stdout)

    atStart = True
    for x in args:
        if not atStart:
            file.write(sep)
        file.write(str(x))
        atStart = False
    file.write(kwargs.pop("end", "\n"))

    if kwargs.pop("flush", False):
        file.flush()

sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

main()
