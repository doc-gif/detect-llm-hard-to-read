
def main():
    
    # n = 6
    # from random import randint
    # selection = '0123456789_X'
    # selection = '012579_X'
    # s = ''.join([selection[randint(0, len(selection) - 1)] for _ in range(n)])
    # if s[0] == '0':
    #     return
    
    s = input()
    n = len(s)
    # print(s)
    
    if n == 1:
        if s in '0_X':
            print(1)
        else:
            print(0)
        return
    
    def canmatchlen2(s1, s2):
        for i in range(2):
            if s1[i] == '_' or s1[i] == s2[i]:
                continue
            else:
                return False
        return True
    
    def count(s):  # with no 'X'
        if s == '0' * n:
            return 1
        if n > 1 and s[0] == '0':  # illegal
            return 0
        # see if can make zzz00, zzz25, zzz50, or zzz75
        last2 = s[n - 2:]
        last2cnts = 0
        for s2 in ['00', '25', '50', '75']:
            if canmatchlen2(last2, s2):
                last2cnts += 1
        if n == 2:
            if canmatchlen2(last2, '00'):
                last2cnts -= 1
            return last2cnts
        # see how many different numbers can the rest make
        otherscnts = 1
        for i in range(n - 2):
            if s[i] == '_':
                if i == 0:
                    otherscnts *= 9
                else:
                    otherscnts *= 10
        return last2cnts * otherscnts
    
    ans = 0
    if 'X' in s:
        for x in [str(z) for z in range(10)]:
            ans += count(s.replace('X', x))
    else:
        ans = count(s)
    print(ans)
    
    # # naive
    # nans = 0
    # xindexes = []
    # for i in range(n):
    #     if s[i] == 'X':
    #         xindexes.append(i)
    # for i in range(int(1e8)):
    #     s2 = str(i)
    #     if len(s2) < n: continue
    #     if len(s2) > n: break
    #     if i % 25 == 0:
    #         ok = True
    #         for j in xindexes:
    #             if s2[xindexes[0]] != s2[j]:
    #                 ok = False
    #         for j in range(n):
    #             if not (s[j] == '_' or s[j] == 'X' or s[j] == s2[j]):
    #                 ok = False
    #         if ok:
    #             nans += 1
    # print(nans)
    # if ans != nans:
    #     print(s)
    
    return

import sys
# input=sys.stdin.buffer.readline #FOR READING PURE INTEGER INPUTS (space separation ok)
input=lambda: sys.stdin.readline().rstrip("\r\n") #FOR READING STRING/TEXT INPUTS.
 
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