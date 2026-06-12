from math import factorial
def solve(n,p,a):
    if p is 9:
        if n>=a[9]:
            return 1
        else:
            return 0
    elif p is 0:
        ans=0
        for i in range(a[0],n):
            z=solve(n-i,1,a)
            z*=factorial(n-1)
            z//=factorial(i)
            z//=factorial(n-1-i)
            ans+=z
        return ans
    else:
        ans=0
        for i in range(a[p],n+1):
            z=solve(n-i,p+1,a)
            z*=factorial(n)
            z//=factorial(i)
            z//=factorial(n-i)
            ans+=z
        return ans
hell=1000000007
n=int(input())
a=input().rstrip().split(' ');
for i in range(0,len(a)):
    a[i]=int(a[i])
ans=0
for i in range(1,n+1):
    ans+=solve(i,0,a)
    ans%=hell
print(ans)