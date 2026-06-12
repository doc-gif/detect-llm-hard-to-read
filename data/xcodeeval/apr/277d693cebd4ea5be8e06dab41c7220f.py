m,s=[int(i) for i in input().split()]
if (s<1 and m>1) or s>9*m:
    print('-1 -1')
elif s==0 and m==1:
    print('0 0')
else:
    n=s//9
    l=s-9*n
    mi=0

    ma0=[str(9)]*n
    if l!=0:
        ma0.append(str(l))
        for i in range(m-n-1):
            ma0.append(str(0))
    else:
        for i in range(m-n):
            ma0.append(str(0))
    ma=''.join(ma0)

    if l!=0:
        for i in range(n):
            mi+=9*10**(i)
        if l!=0 and s>9*(m-1) and n>0:
            mi+=l*10**(n)
        elif l!=0 and s<9*(m-1) and n>0:
            mi+=10**(m-1)+(l-1)*10**(n)
        elif l!=0 and n==0:
            mi+=10**(m-1)+(l-1)
    elif l==0 and s==9*m:
        for i in range(n):
            mi+=10**(m)-1
    else:
        mi+=10**(m-1)
        for i in range(n-1):
            mi+=9*10**(i)
        mi+=8*10**(n-1)
        
    print(int(mi),int(ma))
    