from __future__ import division, print_function
import sys
import os
from io import BytesIO, IOBase
from bisect import bisect_left, bisect_right

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


def print(*args, **kwargs):
    sep = kwargs.pop("sep", " ")
    file = kwargs.pop("file", sys.stdout)
    at_start = True
    for x in args:
        if not at_start:
            file.write(sep)
        file.write(str(x))
        at_start = False
    file.write(kwargs.pop("end", "\n"))
    if kwargs.pop("flush", False):
        file.flush()


if sys.version_info[0] < 3:
    sys.stdin, sys.stdout = FastIO(sys.stdin), FastIO(sys.stdout)
else:
    sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")


def inp():
    return int(input())


def inps():
    return input().strip()


def inlt():
    return list(map(int, input().split()))


def insr():
    s = input().strip()
    return list(s[: len(s)])


def invr():
    return map(int, input().split())


v = []
current = 0
while current < 10**7 + 100:
    v.append(current)
    current += 25
s = input().strip()
n = len(s)
start_idx = bisect_left(v, 10 ** (n - 1))
end_idx = bisect_right(v, 10**n + 1)
if n == 1:
    start_idx = 0
    end_idx = 2
count = 0
for i in range(start_idx, end_idx - 1):
    target = str(v[i])
    valid = True
    X_val = -1
    for j in range(n):
        if s[j] == target[j]:
            continue
        elif s[j] == "_":
            continue
        elif s[j] == "X":
            if X_val == -1:
                X_val = target[j]
            else:
                if target[j] == X_val:
                    continue
                else:
                    valid = False
                    break
        else:
            valid = False
            break
    if valid:
        count += 1
print(count)
