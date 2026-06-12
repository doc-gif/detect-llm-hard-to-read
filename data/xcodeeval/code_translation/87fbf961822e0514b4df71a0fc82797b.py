import sys
import math
import string
import operator
import functools
import fractions
import collections
sys.setrecursionlimit(10**7)
dX= [-1, 1, 0, 0,-1, 1,-1, 1]
dY= [ 0, 0,-1, 1, 1,-1,-1, 1]
RI=lambda: list(map(int,input().split()))
RS=lambda: input().rstrip().split()
#################################################
MAX=1001
s=input().rstrip()
s=s[0]+s[1:-1].replace('dot','.')+s[-1]
s=s[0]+s[1:-1].replace('at','@',1)+s[-1]
print(s)
