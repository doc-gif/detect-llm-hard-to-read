from __future__ import division, print_function
import math
import sys
import os
from io import BytesIO, IOBase
#from collections import deque, Counter, OrderedDict, defaultdict
#import heapq
#ceil,floor,log,sqrt,factorial,pow,pi,gcd
#import bisect
from bisect import bisect_left,bisect_right

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


def print(*args, **kwargs):
	"""Prints the values to a stream, or to sys.stdout by default."""
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


if sys.version_info[0] < 3:
	sys.stdin, sys.stdout = FastIO(sys.stdin), FastIO(sys.stdout)
else:
	sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

input = lambda: sys.stdin.readline().rstrip("\r\n")

def inp():
    return(int(input()))
def inps():
    return input().strip()
def inlt():
    return(list(map(int,input().split())))
def insr():
    s = input().strip()
    return(list(s[:len(s)]))
def invr():
    return(map(int,input().split()))
v=[]
strt=0
while(strt<10**7+100):
    v.append(strt)
    strt+=25
s=input().strip()
n=len(s)
strt=bisect_left(v,10**(n-1))
end=bisect_right(v,10**(n)+1)
if n==1:
    strt=0
    end=2
cnt=0
for i in range(strt,end-1):
    target=str(v[i])
    flag=1
    X=-1
    for i in range(n):
        if s[i]==target[i]:
            continue
        elif s[i]=='_':
            continue
        elif s[i]=='X':
            if X==-1:
                X=target[i]
            else:
                if target[i]==X:
                    continue
                else:
                    flag=0
                    break
        else:
            flag=0
            break
    if flag:
        cnt+=1
print(cnt)