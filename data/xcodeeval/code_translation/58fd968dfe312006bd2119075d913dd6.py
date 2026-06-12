def lucky(x):
    s=str(x)
    return s.count('4')+s.count('7')==len(s)

def Gen_lucky(n):
    if(len(n)==1):
        if(n<"4"):
            return 0
        if(n<"7"):
            return 1
        return 2
    s=str(n)
    if(s[0]<'4'):
        return 0
    if(s[0]=='4'):
        return Gen_lucky(s[1:])
    if(s[0]<'7'):
        return 2**(len(s)-1)
    if(s[0]=='7'):
        return 2**(len(s)-1)+Gen_lucky(s[1:])
    else:
        return 2**len(s)
        

def Form(X,k):
    if(k==0):
        return X
    for i in range(len(X)):
        if(k>=F[len(X)-i-1]):
            h=k//F[len(X)-i-1]
            r=k%F[len(X)-i-1]
            G=list(X[i+1:])
            G.remove(X[i+h])
            G=[X[i]]+G
            return Form(X[:i]+[X[i+h]]+G,r)

p=1

F=[1]
i=1
while(p<=10**15):
    p*=i
    F.append(p)
    i+=1

n,k=map(int,input().split())


    
if(n<=14):
    if(k>F[n]):
        print(-1)
    else:
        L=Form(list(range(1,n+1)),k-1)
        x=0
        for i in range(n):
            if(lucky(i+1) and lucky(L[i])):
                x+=1
        print(x)
else:
    L=Form(list(range(n-14,n+1)),k-1)
    ss=str(n-15)
    x=0
    for i in range(1,len(ss)):
        x+=2**i
    x+=Gen_lucky(ss)
    for i in range(n-14,n+1):
        if(lucky(L[i-n+14]) and lucky(i)):
            x+=1
    print(x)
       
