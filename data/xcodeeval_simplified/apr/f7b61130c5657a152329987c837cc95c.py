import sys
import os
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


def MI(num, mod):
    NUM, MOD = num, mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = num // mod
        num, mod = mod, num % mod
        x, x_old = x_old - q * x, x
        y, y_old = y_old - q * y, y
    if num != 1:
        print(f"\nNO MI. However, the GCD of {NUM} and {MOD} is {num}\n")
    else:
        MI = (x_old + MOD) % MOD
        return MI


MOD = int(1e9) + 7
n, k = map(int, input().split())
if k == 0:
    print("1")
elif k >= n:
    ans = pow(2, n, MOD)
    print(ans)
elif k == n - 1:
    ans = pow(2, n, MOD)
    ans = (ans - 1 + MOD) % MOD
    print(ans)
else:
    if n == 1:
        print("2")
    else:
        ans = 1
        numerator = 1
        for i in range(2, n + 1):
            numerator = (numerator * i) % MOD
        denominator1 = 1
        denominator2 = 1
        for i in range(2, n):
            denominator2 = (denominator2 * i) % MOD
        extra1 = 2
        extra2 = n - 1
        for i in range(1, k + 1):
            val1 = MI(denominator1, MOD)
            add = (numerator * val1) % MOD
            val2 = MI(denominator2, MOD)
            add = (add * val2) % MOD
            ans = (ans + add) % MOD
            denominator1 = (denominator1 * extra1) % MOD
            extra2_inverse = MI(extra2, MOD)
            denominator2 = (denominator2 * extra2_inverse) % MOD
        print(ans)
