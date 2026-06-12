from __future__ import print_function
from math import *
from collections import defaultdict, deque
import os
import random
import sys
from io import BytesIO, IOBase
#import time
 
def main():
    pass
 
# region fastio
 
BUFSIZE = 8192
def lcm(a,b):
    return (a*b)//gcd(a,b)
def ceilDiv(a,b):
    if a%b==0:
        return a//b
    else:
        return a//b+1
 
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
class myDict:
    def __init__(self,func):
        self.RANDOM = random.randint(0,1<<32)
        self.default=func
        self.dict={}
    def __getitem__(self,key):
        myKey=self.RANDOM^key
        if myKey not in self.dict:
            self.dict[myKey]=self.default()
        return self.dict[myKey]
    def __setitem__(self,key,item):
        myKey=self.RANDOM^key
        self.dict[myKey]=item
    def getKeys(self):
        return [self.RANDOM^i for i in self.dict]
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
#sys.stdin, sys.stdout =open("test.txt","r"),open("result.txt","w")
#ini=time.time()
input = lambda: sys.stdin.readline().rstrip("\r\n")
mod=10**9+7
############ ---- Input Functions ---- ############
def inp():
    return(int(input()))
def inlt():
    return(list(map(int,input().split())))
def insr():
    s = input()
    return(list(s[:len(s) ]))
def invr():
    return(map(int,input().split()))
n,m=invr()
dp=[0]
s=set()
for i in range(1,21):
    for j in range(1,1+m):
        s.add(j*i)
    dp.append(len(s))
del(s)
ans=1
#print(dp)
v=[0]*(1+n)
for i in range(2,n+1):
    if not v[i]:
        j=1
        while i**j<=n:
            v[i**j]=1
            j+=1
        #print(j)
        ans+=dp[j-1]
print(ans)