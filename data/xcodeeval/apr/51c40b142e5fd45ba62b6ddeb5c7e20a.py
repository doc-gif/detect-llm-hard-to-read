t=int(input())
while(t):
    t-=1
    n=int(input())
    l=list(map(int,input().strip().split()))
    ct=0

    for i in range(1,n):
        if(l[i]==1):
            if(l[i-1]==2):
                ct+=3
            else:
                ct+=4
        elif(l[i]==2):
            if(l[i-1]==1):
                if(i>=2 and l[i-2]==3):
                    ct+=2
                else:
                    ct+=3
            else:
                ct=-1
        else:
            if(l[i-1]==1):
                ct+=4
            else:
                ct=-1
        if(ct==-1):
            print('Infinite')
            break
    if(ct!=-1):
        print('Finite')
        print(ct)
