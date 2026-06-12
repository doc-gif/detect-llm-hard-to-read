def soch(n,k):
    r,e=max(k,n-k),min(k,n-k)
    ans=1
    ansv=1
    for i in range(r+1,n+1):
        ans*=i
    for i in range(1,e+1):
        ansv*=i
    return ans//ansv
n,k=map(int,input().split())
ans=1
s=1
y=k-(k-n//2)
h=min(n//2+(n%2==1)+1,k+1)
if k<n:
    if k+1>=h:
        for i in range(1,min(h,k+1)):
            s=(s*(n-i+1))//i
            ans+=s%(10**9+7)
            if y>0 and i>y and (h-1)!=i:
                ans+=s
        print(ans%(10**9+7))
    else:
        for i in range(1,n-k):
            s=(s*(n-i+1))//i
            ans+=s%(10**9+7)
            if y>0 and i>y and (h-1)!=i:
                ans+=s
        print(pow(2,n,10**9+7)-ans%(10**9+7))        
else:
    print(pow(2,n,10**9+7))