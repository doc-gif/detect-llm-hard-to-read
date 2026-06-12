# import io, os
# input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
import sys
# sys.stdin=open('input.txt','r')
# sys.stdout=open('output.txt','w')
input=sys.stdin.readline
# sys.setrecursionlimit(300010)
MOD = 1000000007
MOD2 = 998244353
ii = lambda: int(input().strip('\n'))
si = lambda: input().strip('\n')
dgl = lambda: list(map(int,input().strip('\n')))
f = lambda: map(int, input().strip('\n').split())
il = lambda: list(map(int, input().strip('\n').split()))
ls = lambda: list(input().strip('\n'))
let = 'abcdefghijklmnopqrstuvwxyz'
d=dict()
sieve=[1]*(1000005)
for i in range(2,10**6+4):
    if sieve[i]:
        d[i]=[i]
        for j in range(i*2,10**6+4,i):
            if j in d:
                d[j].append(i)
            else:
                d[j]=[i]
            sieve[j]=0
n=ii()
ans=set(d[n])
cnt=[n]
for i in range(n-1,-1,-1):
    if any(i in ans for i in d[i]):
        continue
    else:
        ans=ans.union(d[i])
        cnt.append(i)
    if len(cnt)==3:
        break
prod=1
for i in cnt:
    prod*=i
print(prod)