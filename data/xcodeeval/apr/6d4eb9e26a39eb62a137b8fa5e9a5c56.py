a,b,f,k=map(int,input().split())
i=0
bi=b
ans=0
while i<k:
    if f>bi:
        print(-1)
        exit()
    else:
        bi-=f
    if k-i==1:
        if a-f>bi:
            bi=b
            ans+=1
            if a-f>bi:
                print(-1)
                exit()
    else:
        i+=1
        if 2*(a-f)>bi:
            bi=b
            ans+=1
            if 2*(a-f)>bi:
                print(-1)
                exit()
        bi-=2*(a-f)
        if k-i==1:
            if f>bi:
                bi=b
                ans+=1
                if f>bi:
                    print(-1)
                    exit()
        else:
            if 2*f>bi:
                bi=b
                ans+=1
                if 2*f>bi:
                    print(-1)
                    exit()
            else:
                bi-=f
        i+=1
print(ans)
