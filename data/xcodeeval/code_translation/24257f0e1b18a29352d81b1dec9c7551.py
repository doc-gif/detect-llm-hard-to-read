n,k=map(int,input().split(' '))
count=0
if n==2:
    print(6)
else:
    i=3
    while i<=n:
        count=count+3
        i=i+1
    count=count+6
    
    if n%2==0 and k!=1:
        if int(n/2)<k:
            print(count+n-k)
        else:
            print(count+k-1)
    elif n%2!=0 and k!=1:
        if int((n+1)/2)<k:
            print(count+n-k)
        else:
            print(count+k-1)
    elif k==1:
        print(count)
    