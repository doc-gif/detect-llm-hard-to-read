from cmath import inf
from re import L, T
from telnetlib import TN3270E
def swap(a,b):
    a = a^b
    b = a^b
    a = a^b
    return a,b
    # call using a,b = swap(a,b)
def even(a):
    if a&1:
        return False
    return True
def gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

def lcm(x, y):
   lcm = (x*y) // gcd(x,y)
   return lcm

# it will return index of "key" in "sorted list". 
def BS_elemPosi(low, high, key, li):  
    while low<high:
        mid = (low+high)//2
        if key>=li[mid]:
            low = mid+1
        else:
            high = mid
    return low

def swap(arr, i,j):
    tmp = arr[i]
    arr[i] = arr[j]
    arr[j] = tmp

def perm(li,arr, curr_indx=0):
    if curr_indx==len(arr)-1:
        li.append("".join(arr))
    for i in range(curr_indx,len(arr)):
        swap(arr,curr_indx,i)
        perm(li,arr,curr_indx+1)
        swap(arr,curr_indx,i)

import sys
input = sys.stdin.readline
###########################(CODE)#######################################
for _ in range(int(input())):
    n = int(input())
    if n==1:
        print(1)
    elif n%2==0:
        print(n*2-1)
    else:
        print(n*2+1)
#######################################################################