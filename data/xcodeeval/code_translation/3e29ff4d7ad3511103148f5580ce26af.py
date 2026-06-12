a, b, f, k=map(int,input().split())
d=b
n=0
s=0
x=a-f
d -= f
if (x*2>b) or (f*2>b):
    if k<3:
        if k==1:
            if a<=b:
                print(0)
            elif (f<=b) and (x<=b):
                print(1)
            else:
                print(-1)
        if k==2:
            if a+x<=b:
                print(1)
            elif (f<=b) and (x*2<=b):
                print(2)
            else:
                print(-1)
    else:
        print(-1)
else:
    while n<k:
        if (n+1==k):
            if (d<x):
                s+=1
            break
        if d<x*2:
            s+=1
            d=b
        n+=1
        d-=x*2
        if (n+1==k):
            if (d<f):
                s+=1
            break
        if d<f*2:
            s+=1
            d=b
        n+=1
        d-=f*2
    print(s)
