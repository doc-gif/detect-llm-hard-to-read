n=int(input())
l=list(map(int,input().split()))
emp=[]
for i in range(n):
    c=0
    for j in range(n):
        if j<=i:
            c+= l[j]*i*4
        else:
            c+=l[j]*j*4
    emp.append(c)
print(min(emp))
    
            
            