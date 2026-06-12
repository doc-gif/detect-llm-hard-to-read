def soe(n):
    primes=[True]*(n+1)
    primes[0]=primes[1]=False
    i=4 
    while i<n:
        primes[i]=False
        i+=2 
    i=3 
    while i*i<=n:
        for j in range(i*i,n,2*i):
            primes[j]=False
        i+=2 
    ans=[]
    for i in range(len(primes)):
        if primes[i]:
            ans.append(i)
    return ans
prim=soe(10**8)
n=int(input())
ct=0 
f=-1
for i in prim:
    if n%i==0:
        ct+=1 
        f=i
if ct>=2:
    print(1)
elif ct==1:
    print(f)
else:
    print(n)