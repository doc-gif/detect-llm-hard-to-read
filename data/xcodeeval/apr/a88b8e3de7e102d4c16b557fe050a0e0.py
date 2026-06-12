n,m,k,x,y=list(map(int,input().split()))
if n>2:
    if n*m<k:
        b=(k-n*m)//((n-1)*m)
        k=k-n*m-b*(n-1)*m
        m2=b+1
        m1=(m2+1)//2
        if x==1 or x==n:
            m3=m1
        else:
            m3=m2
        if b%2==0:
            i=n-1
            c=-1
        else:
            if x==1:
                m3=m3+1
            i=2
            c=1
        j=1
        if k>0:
            m2=m2+1
        while k>0:
            if x==i and y==j:
                m3=m3+1
            k=k-1
            j=j+1
            if j==m+1:
                j=1
                i=i+c
        print(m2,m1,m3)
    elif k==n*m:
        print(1,1,1)
    else:
        if x<=k//m:
            print(1,0,1)
        elif x==k//m+1 and y<=k%m:
            print(1,0,1)
        else:
            print(1,0,0)
elif n==2:
    m2=k//(n*m)
    m3=m2
    m1=m2
    k=k%(n*m)
    if k>0:
        m2=m2+1
    i=1
    j=1
    while k>0:
        if x==i and y==j:
            m3=m3+1
        j=j+1
        if j==m+1:
            j=1
            i=i+1
    print(m2,m1,m3)
else:
    if k%m==0:
        print(k//m,k//m,k//m)
    else:
        if y<=k%m:
            print(k//m+1,k//m,k//m+1)
        else:
            print(k//m+1,k//m,k//m)