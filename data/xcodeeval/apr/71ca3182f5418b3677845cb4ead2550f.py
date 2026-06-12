import math,sys
import heapq
from fractions import Fraction
from collections import Counter,defaultdict
def li(): return list(map(int,sys.stdin.readline().split()))
def ls(): return list(map(int,list(input())))
def la(): return list(input())
def ii():  return int(input())
def dic(x): return defaultdict(lambda: x) 
def isPrime(n):
    i= 2
    if n == 1:
        return False
    while i <= int(math.sqrt(n)):
        if n%i == 0:
            return False
        i = i + 1
    return True
def gcd(a,b):
    if b == 0:
        return a
    return gcd(b,a%b)
def binarySearch(arr, x): 
    l,r = 0,len(arr)-1
    while l <= r: 
        mid = l + (r - l) // 2; 
        if arr[mid] == x: 
            return True 
        elif arr[mid] < x: 
            l = mid + 1
        else: 
            r = mid - 1
    return False
minn = float("inf")
x ,y ,n= li()
for i in range(1,n):
    if abs(Fraction(x,y)-Fraction(x,y).limit_denominator(i)) <minn :
        minn = abs(Fraction(x,y)-Fraction(x,y).limit_denominator(i))
        ans = Fraction(x,y).limit_denominator(i)
print(ans)


