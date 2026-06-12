z,zz=input,lambda:list(map(int,z().split()));
szz,dgraphs,mod=lambda:sorted(zz()),{},10**9+7
from string import *
from collections import *
from queue import *
from sys import *
from collections import *
from math import *
from heapq import *
from itertools import *
from bisect import *
from collections import Counter as cc
from math import factorial as f
def lcd(xnum1,xnum2):return (xnum1*xnum2//gcd(xnum1,xnum2))
def prime(x):
    p=ceil(x**.5)+1
    for i in range(2,p):
        if x%i==0 and x!=2:return 0
    return 1
def dfs(u,visit,graph):
    visit[u]=True
    for i in graph[u]:
        if not visit[i]:
            dfs(i,visit,graph)
################################################################################

"""

led=(6,2,5,5,4,5,6,3,7,6)

color4=["G", "GB", "YGB", "YGBI", "OYGBI" ,"OYGBIV",'ROYGBIV' ]

"""

###########################---START-CODING---####################################

l=zz()

ans=-1

for i,j in enumerate(l):
    p=l[:]
    
    p[i]=0
    n=j//14
    ex=j%14
    
    m=i+1
    for _ in range(ex):
        if m==13:
            p[m]=(p[m]+1)
            m=0
        else:
            p[m]=(p[m]+1)
            m+=1

    for k in range(14):
        p[k]=(p[k]+n)

    t=0
    for i in p:
        if i%2==0:
            t+=i

    if t>ans:
        ans=t
print(ans) 

        
    
    
    

    








        

