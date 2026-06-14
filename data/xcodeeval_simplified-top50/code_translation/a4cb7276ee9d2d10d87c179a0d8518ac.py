import sys
import math
import heapq
from sys import stdin, stdout
import bisect
def modinv(n, p):
    return pow(n, p - 2, p)
def cin():
    return map(int, sin().split())
def ain():
    return list(map(int, sin().split()))
def sin():
    return input()
def inin():
    return int(input())
def Divisors(n):
    l = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            if n // i == i:
                l.append(i)
            else:
                l.append(i)
                l.append(n // i)
    return l
def main():
    n = inin()
    a = ain()
    x = n // 2
    p = []
    q = []
    if n % 2 == 1:
        y = x + 1
    else:
        y = x
    i = 0
    j = +1
    f = -1
    ans = j = 0
    pp = []
    qq = []
    for i in range(n):
        if a[i] != 0:
            if a[i] % 2 == 1:
                y -= 1
            else:
                x -= 1
            if f == -1 or a[i] % 2 ^ f == 0:
                if a[i] % 2 == 1:
                    if f == -1:
                        pp.append(j)
                    else:
                        p.append(j)
                    j = 0
                    f = a[i]
                else:
                    if f == -1:
                        qq.append(j)
                    else:
                        q.append(j)
                    j = 0
            else:
                ans += 1
                j = 0
            f = a[i] % 2
        else:
            j += 1
    if f % 2 == 0:
        qq.append(j)
    else:
        pp.append(j)
    p.sort()
    q.sort()
    an = ans
    xx = x
    yy = y
    pp.sort()
    qq.sort()
    for i in pp:
        y -= i
        if i == 0:
            continue
        if y < 0:
            ans += 1
    for i in qq:
        x -= i
        if i == 0:
            continue
        if x < 0:
            ans += 1
    for i in p:
        y -= i
        if i == 0:
            continue
        if y < 0:
            ans += 2
    for i in q:
        x -= i
        if i == 0:
            continue
        if x < 0:
            ans += 2
    x = xx
    y = yy
    for i in p:
        y -= i
        if y < 0:
            y += i
            an += 2
    for i in q:
        x -= i
        if x < 0:
            x += i
            an += 2
    for i in pp:
        y -= i
        if y < 0:
            y += i
            an += 1
    for i in qq:
        x -= i
        if x < 0:
            x += i
            an += 1
    if ans == 0 and n > 1:
        ans = 1
    print(min(an, ans))
py2 = round(0.5)
if py2:
    from future_builtins import ascii, filter, hex, map, oct, zip
    range = xrange
import os
from io import IOBase, BytesIO
BUFSIZE = 8192
class FastIO(BytesIO):
    newlines = 0
    def __init__(self, file):
        self._file = file
        self._fd = file.fileno()
        self.writable = "x" in file.mode or "w" in file.mode
        self.write = super(FastIO, self).write if self.writable else None
    def _fill(self):
        s = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
        self.seek((self.tell(), self.seek(0, 2), super(FastIO, self).write(s))[0])
        return s
    def read(self):
        while self._fill():
            pass
        return super(FastIO, self).read()
    def readline(self):
        while self.newlines == 0:
            s = self._fill()
            self.newlines = s.count(b"\n") + (not s)
        self.newlines -= 1
        return super(FastIO, self).readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.getvalue())
            self.truncate(0), self.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        if py2:
            self.write = self.buffer.write
            self.read = self.buffer.read
            self.readline = self.buffer.readline
        else:
            self.write = lambda s: self.buffer.write(s.encode("ascii"))
            self.read = lambda: self.buffer.read().decode("ascii")
            self.readline = lambda: self.buffer.readline().decode("ascii")
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")
class ostream:
    def __lshift__(self, a):
        sys.stdout.write(str(a))
        return self
cout = ostream()
endl = "\n"
def readnumbers(zero=0):
    conv = ord if py2 else lambda x: x
    A = []
    numb = zero
    sign = 1
    i = 0
    s = sys.stdin.buffer.read()
    try:
        while True:
            if s[i] >= b"0"[0]:
                numb = 10 * numb + conv(s[i]) - 48
            elif s[i] == b"-"[0]:
                sign = -1
            elif s[i] != b"\r"[0]:
                A.append(sign * numb)
                numb = zero
                sign = 1
            i += 1
    except:
        pass
    if s and s[-1] >= b"0"[0]:
        A.append(sign * numb)
    return A
if __name__ == "__main__":
    main()