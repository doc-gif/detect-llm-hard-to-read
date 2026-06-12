# ------------------- fast io --------------------
from __future__ import division, print_function
import os
import sys
from io import BytesIO, IOBase
import itertools
if sys.version_info[0] < 3:
    input = raw_input
    range = xrange
 
    filter = itertools.ifilter
    map = itertools.imap
    zip = itertools.izip   
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
if os.path.exists('input.txt'):
    sys.stdin = open('input.txt','r')
    sys.stdout = open('output.txt','w')
 
 
# ----------------- fast io --------------------
from math import *
from itertools import * # chain,groupby,permutations,combinations
from collections import * #deque
from bisect import *
from heapq import *
from random import *
 
 


 
"""
 
def gcd(x, y):
    
    while y:
        x, y = y, x % y
    return x
 
 
def prod(a, mod=10**9+7):
    ans = 1
    for each in a:
        ans = (ans * each) % mod
    return ans
 
def lcm(a, b): return a * b // gcd(a, b)
 
def binary(x, length=16):
    y = bin(x)[2:]
    return y if len(y) >= length else "0" * (length - len(y)) + y
 
 
def powerset(s):
    n=len(s)
    
    return chain.from_iterable(combinations(s,r) for r in range(1,n))
 
def binarySearch(arr,x): 
    l=0
    r=len(arr)-1
    while l <= r: 
  
        mid = l + (r - l) // 2; 
        if arr[mid] == x: 
            return mid 
        elif arr[mid] < x: 
            l = mid + 1
        else: 
            r = mid - 1
    return -1
 
def prime(n): #array of prime numbers
    arr = [1]*(n+1)
    arr[0] = arr[1] = 0
    p=2
    while p*p<=n:
        if arr[p]:
            for i in range(p * 2, n + 1, p):
                arr[i] = 0
            p+=1
 
 
    return arr

def prime(n):
    # Returns  a list of primes < n 
    sieve = [True] * n
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3,n,2) if sieve[i]]
 
   
 
 
def palindrome(string,start,end):
    if start==end:
        return True
    if end==1:
        return True
    return string[start]==string[end-1] and palindrome(string,start+1,end-1)
 
def binomialCoeff(n, k):
 
    
    C = [0 for i in range(k+1)]
    C[0] = 1  
 
    for i in range(1, n+1):
 
        
        j = min(i, k)
        while (j > 0):
            C[j] = C[j] + C[j-1]
            j -= 1
 
    return C[k]


def binary_search(array):

    def condition(value) -> bool:
        pass

    left, right = min(search_space), max(search_space) # could be [0, n], [1, n] etc. Depends on problem
    while left < right:
        mid = left + (right - left) // 2
        if condition(mid):
            right = mid
        else:
            left = mid + 1
    return left

prime_dict = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13, 'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37, 'm': 41, 'n': 43, 'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79, 'w': 83, 'x': 89, 'y': 97, 'z': 101}

 
"""
 
#----# My Functions

inf = float("inf")
mod = 10**9+7
noyes = ["NO","YES"]
yesno = ["YES","NO"]
def aa(): 
    return int(input())

def bb(): 
    return list(map(int,input().split()))

def cc():  
    s = input()
    return list(s)

def dd(): 
    return map(int,input().split())

def put(i,val):
    print("Case #",i,":",val)

def swap(arr,i,j):
    arr[i],arr[j] = arr[j],arr[i]

def power(base, exp, mod = mod):
    ans = 1

    while exp:
        lastbit = exp & 1
        if lastbit:
            ans = (ans * base)%(mod)

        base=(base*base)%mod
        exp>>=1

    return ans%mod
#----#



def koi_coding_sikha_do():
    
    n = aa()
    if n%2==0:
        print(2**n)
    else:
        print(2**n - 1)




    

    




    

    


onlyone = 0 
t=1 if onlyone else int(input())
while(t):
    
    koi_coding_sikha_do()
    
    t-=1
 

 
"""
__________          __  .__                              __    __             _________                          
\______   \___.__._/  |_|  |__   ____   ____             \ \   \ \            \_   ___ \     .__         .__     
 |     ___<   |  |\   __\  |  \ /  _ \ /    \             \ \   \ \           /    \  \/   __|  |___   __|  |___ 
 |    |    \___  | |  | |   Y  (  <_> )   |  \            / /   / /           \     \____ /__    __/  /__    __/ 
 |____|    / ____| |__| |___|  /\____/|___|  /           /_/   /_/             \______  /    |__|        |__|    
           \/                \/            \/                                         \/                         
 
 
Unke aakhon me aasu aur chahre pe hasi hai......lagta hai unki lulli unki zip me phasi hai
"""
