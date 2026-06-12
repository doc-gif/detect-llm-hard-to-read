from math import gcd

n, m = map(int, input().split())
ans=0
cur=m
g=2
q=m*m
for i in range(2, n+1):
    if gcd(g, i)==1 and g < 10 ** 13:
        g*=i
    cur*=m//g
    cur=cur%998244353
    ans+=q-cur
    q*=m
    q=q%998244353
    ans=ans%998244353
print(ans%998244353)