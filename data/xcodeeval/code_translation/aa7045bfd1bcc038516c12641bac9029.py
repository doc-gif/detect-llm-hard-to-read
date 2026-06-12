n,m=map(int,input().split())
max=0
min=0
if (m==0 and n!=1) or m>9*n:
    print(-1,-1)
elif n==1 and m==0:
    print(0,0)
else:
    min=10**(n-1)
    for i in range(m-1):
        a=(i//9)
        min+=10**a
    max=0
    for i in range(m):
      b=(n-1-i//9)
      max+=10**b
    print(min,max)
