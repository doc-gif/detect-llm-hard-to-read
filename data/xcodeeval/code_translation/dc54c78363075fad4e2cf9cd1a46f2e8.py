n,k=map(int,input().split())
l=list(map(int,input().split()))
b=1
maxx=0
for b in range(1,n+1):
    x=[0 for i in range(n)]
    temp=[]
    c=b
    c1=b
    i=0
    j=0
    while c<=n:
        x[c-1]=1
        i+=1
        c=b+i*k
    while c1>=1:
        x[c1-1]=1
        j-=1
        c1=b+j*k
    f1=0
    f2=0
    for i in range(n):
        if x[i] == 0:
            if l[i] == 1:
                f1+=1
            else:
                f2+=1
    maxx=max(maxx,abs(f1-f2))
print(maxx)        

