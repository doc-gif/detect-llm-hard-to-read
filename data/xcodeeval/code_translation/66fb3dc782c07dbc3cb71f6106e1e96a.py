n,k=map(int,input().split())
a=[0]*k
for i in range(k):
    if n%k==0:
        exit(print('Yes'))
    if a[n%k]!=1:
        a[n%k]=1
        n+=n%k
    else:
        exit(print('No'))
print('Yes')
        