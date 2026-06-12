from sys import stdin
input=stdin.readline
w,h=map(int,input().split())
h,w=sorted([w,h])
ans=1
mod=998244353
for i in range(w):
    ans+=2**i
for i in range(h):
    ans+=ans
print(ans%mod)