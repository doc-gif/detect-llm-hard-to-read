k=int(input())
for i in range(1,k):
    z,a=i,[]
    for j in range(k-1):
        p,s=z,""
        while p:
            s=str(p%k)+s
            p//=k
        z+=i
        a.append(s)
    print(*a)

    
