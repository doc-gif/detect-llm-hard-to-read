
def getint():
    return [int(i) for i in input().split()]
def get():
    return int(input())
def getstr():
    return [i for i in input().split()]
def S():
    for test in range(int(input())):
        solve()
import math
import itertools as it
import bisect
import time
import collections as ct

def lower_bound(a,x):
    l=-1
    r=len(a)
    while l+1!=r:
        mid=l+r>>1
        if a[mid]<x:
            l=mid
        else:
            r=mid
    return r
def upper_bound(a,x):
    l=-1
    r=len(a)
    while l+1!=r:
        mid=l+r>>1
        if a[mid]<=x:
            l=mid
        else:
            r=mid
    return r
def solve():
    n=get()
    print(3*n-2)


S()
