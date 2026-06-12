n=int(input())
l=int(input())
r=int(input())
a=[]
t=1
for i in range(l):
    a.append(t)
    t=t*2
b=[]*n
i=0
while(i<n-l+1):
    b.append(a[0])
    i=i+1
j=1 
for j in range(l-1):
    b.append(a[j+1])    
sum=0
for i in range(len(b)):
    sum=sum+b[i]
    
c=[]
k=1
for i in range(r):
    c.append(k)
    k=k*2
u=[]*n
y=0
while(y<n-r+1):
    u.append(c[len(c)-1])
    y=y+1
for g in range(r-1):
    u.append(c[g])
    

sums=0
for i in range(len(u)):
    sums=sums+u[i]
    
print(sum,sums)