a,b,f,k=map(int,input().split())
#if max(2*f,2*(a-f))>b and k!=1:
#    print('-1')
if k==1 and max(f,a-f)>b:
    print('-1')
else:
    m=b
    dir=1
    l=0
    pos=1
    x=0
    z=0
    while l<k:
        if pos==1 and m>=f and dir==1:
            m-=f
            dir=1
            pos=2
        elif pos==2 and dir==1:
            if k-l>1 and m>=2*(a-f):
                dir=2
                pos=2
                l+=1
                m-=(2*(a-f))
            elif k-l==1 and m>=(a-f):
                l+=1
            else:
                m=b
                x+=1
        elif pos==2 and dir==2:
            if k-l>1 and m>=2*(f):
                dir=1
                pos=2
                l+=1
                m-=(2*(f))
            elif k-l==1 and m>=(f):
                l+=1
            else:
                m=b
                x+=1 
        else:
            z=1
            break
    if z==0:
        print(x)
    else:
        print('-1')