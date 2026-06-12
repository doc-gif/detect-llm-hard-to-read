"""
    This template is made by Satwik_Tiwari.
    python programmers can use this template :)) .
"""

#===============================================================================================
#importing some useful libraries.

import sys
import bisect
import heapq
from math import *
from collections import Counter as counter  # Counter(list)  return a dict with {key: count}
from itertools import combinations as comb # if a = [1,2,3] then print(list(comb(a,2))) -----> [(1, 2), (1, 3), (2, 3)]
from itertools import permutations as permutate
from bisect import bisect_left as bl #
from bisect import bisect_right as br
from bisect import bisect

#===============================================================================================
#some shortcuts

mod = pow(10, 9) + 7
def inp(): return sys.stdin.readline().strip() #for fast input
def out(var): sys.stdout.write(str(var))  #for fast output, always take string
def lis(): return list(map(int, inp().split()))
def stringlis(): return list(map(str, inp().split()))
def sep(): return map(int, inp().split())
def strsep(): return map(str, inp().split())
def graph(vertex): return [[] for i in range(0,vertex+1)]
def zerolist(n): return [0]*n
def nextline(): out("\n")  #as stdout.write always print sring.
def testcase(t):
    for p in range(t):
        solve()
def printlist(a) :
    for p in range(0,len(a)):
        out(str(a[p]) + ' ')
def lcm(a,b): return (a*b)//gcd(a,b)


#===============================================================================================
# code here ;))
def sieve(a): #O(n loglogn) nearly linear
    #all odd mark 1
    for i in range(3,((10**6)+1),2):
        a[i] = 1
    #marking multiples of i form i*i 0. they are nt prime
    for i in range(3,((10**6)+1),2):
        for j in range(i*i,((10**6)+1),i):
            a[j] = 0
    a[2] = 1 #special left case
    return (a)


a = [0]*((10**8)+1)
a = sieve(a)

def func(d):
    ans = 1
    if(d%2 == 0):
        x = 1
        while(d%(2**x) == 0):
            x+=1
        ans *= x
    for i in range(3,d+1,2):
        if(a[i] == 0 or d%i == 1):
            continue
        elif(d%i == 0):
            x = 1
            while(d%(i**x)==0):
                x+=1
            ans *=x
    return ans

def solve():
    a,b,c = sep()
    ans = 0
    for i in range(1,a+1):
        for j in range(1,b+1):
            for k in range(1,c+1):
                ans += (func(i*j*k))%1073741824
    print(ans%1073741824)

testcase(1)

