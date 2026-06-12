n,k=map(int,input().split())
k=10**k
s=n*k
while n*k>0:
    if n>k:
        n=n%k
    else:
        k=k%n
D=s//(n+k)
print(D)