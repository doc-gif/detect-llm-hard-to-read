
def naive(n, m):
    vi = set()
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            vi.add(i ** j)
            # print(i ** j)
    return len(vi)

# find unique cnts in this table:
#     1 2 3  4.. m
#     2 4 6  8..
#     3 6 9  12
#     4 8 12 16
#     n 2n 3n .. nm
# Note that n is only up to ~ 20 while m can go to 1e6.
tableCnts = [-1] * 22

def main():
    
    n, m = readIntArr()
    
    tableVi = [False] * (22 * (m + 1) + 5)
    cnt = 0
    for i in range(1, 22):
        for j in range(1, m + 1):
            x = i * j
            if tableVi[x] == False:
                tableVi[x] = True
                cnt += 1
        tableCnts[i] = cnt
    
    
    ans = 1 # for 1st row
    vi = [False] * (n + 1)
    
    for i in range(2, n + 1):
        if vi[i] == False:
            N = 0
            j = i
            while j <= n:
                vi[j] = True
                N += 1
                j *= i
            ans += tableCnts[N]
            # print('i:{} N:{} change:{}'.format(i, N, tableCnts[N]))
    print(ans)
    
    # print('naive:{}'.format(naive(n, m)))
    
    return
 
import sys
input=sys.stdin.buffer.readline #FOR READING PURE INTEGER INPUTS (space separation ok)
# input=lambda: sys.stdin.readline().rstrip("\r\n") #FOR READING STRING/TEXT INPUTS.
 
def oneLineArrayPrint(arr):
    print(' '.join([str(x) for x in arr]))
def multiLineArrayPrint(arr):
    print('\n'.join([str(x) for x in arr]))
def multiLineArrayOfArraysPrint(arr):
    print('\n'.join([' '.join([str(x) for x in y]) for y in arr]))
 
def readIntArr():
    return [int(x) for x in input().split()]
# def readFloatArr():
#     return [float(x) for x in input().split()]
 
def makeArr(defaultValFactory,dimensionArr): # eg. makeArr(lambda:0,[n,m])
    dv=defaultValFactory;da=dimensionArr
    if len(da)==1:return [dv() for _ in range(da[0])]
    else:return [makeArr(dv,da[1:]) for _ in range(da[0])]
 
def queryInteractive(a, b, c):
    print('? {} {} {}'.format(a, b, c))
    sys.stdout.flush()
    return int(input())
 
def answerInteractive(x1, x2):
    print('! {} {}'.format(x1, x2))
    sys.stdout.flush()
 
inf=float('inf')
# MOD=10**9+7
# MOD=998244353
 
from math import gcd,floor,ceil
import math
# from math import floor,ceil # for Python2
 
for _abc in range(1):
    main()