from collections import*
n,m=map(int,input().split())
C=lambda k:Counter(i*i%m for i in range(1,k+1))
c,d=C(m),C(n%m)
r=Counter(dict((k,n//m*c[k]+d[k])for k in c))
print(sum(r[k]*r[(m-k)%m]for k in r))