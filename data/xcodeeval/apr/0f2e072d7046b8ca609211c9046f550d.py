#!/usr/bin/env python
import collections
import os
import sys
from io import BytesIO, IOBase
from bisect import bisect_left
from math import gcd,log,ceil
from collections import Counter
from pprint import pprint
import heapq
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
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")
 # endregion
 


def two_power(n):
    dp = [1 for _ in range(n+1)]

    mod = int(1e9+7)
    for i in range(1,n+1):
        dp[i] = (dp[i-1]*2) % mod 

    # print(dp)
    return dp

def main():
    n = int(input())
    if n == 1:
        print(6)
        return 
    powers = two_power(60)
    powers = two_power((powers[n]-2)*2+1)
    # ans = 0 
    mod = int(1e9+7)
    # ans += (4*powers[n] * (powers[n-1]))%mod
    # ans += (2 *sum(powers[i] for i in range(1,n+1,2))* (powers[n-2] - powers[(n-2)//2])) % mod 

    # # print(ans)
    # print((4*6*6*4*4*4*4)/24576)
    # print(24576//(6*6*4*4*4*4))

    ans = 6 

    
    # print((ans * (4 ** (powers[n]-2) ) %mod)%mod)

    # print((ans * (powers[(powers[n]-2)*2] %mod)%mod))

    a = (pow(2,n,mod) - 2)%mod
    b = pow(4,a,mod) %mod 
    print((b*ans)%mod)

    # print(ans % mod)


if __name__ == "__main__":
    for _ in range(1):
        main()



