from sys import stdin, stdout
from collections import Counter, defaultdict
pr=stdout.write
import heapq
raw_input  = stdin.readline
def ni():
    return int(raw_input())


def li():
    return list(map(int,raw_input().split()))


def pn(n):
    stdout.write(str(n)+'\n')


def pa(arr):
    pr(' '.join(map(str,arr))+'\n')

# fast read function for total integer input

def inp():
    # this function returns whole input of
    # space/line seperated integers 
    # Use Ctrl+D to flush stdin.
    return (map(int,stdin.read().split()))
    
range = xrange # not for python 3.0+


    

# main code

fac=[1]*1005
mx=1005
mod=998244353
for  i in range(1,mx):
    fac[i]=(fac[i-1]*i)%mod
def inv(x):
    return pow(x,mod-2,mod)
def ncr(n,r):
    num=fac[n]
    den=(fac[r]*fac[n-r])%mod
    return (num*inv(den))%mod
def fun(x,y):
    ans=0
    for i in range(min(x,y)+1):
        ans=(ans+(fac[i]*ncr(x,i)*ncr(y,i))%mod)%mod
    return ans
a,b,c=li()
pn((fun(a,b)*fun(b,c)*fun(a,c))%mod)

