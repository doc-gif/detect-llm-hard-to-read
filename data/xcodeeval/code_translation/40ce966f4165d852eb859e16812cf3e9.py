import math
n=int(input())
x=n
f=1
a=[x]
for i in range(2,int(math.sqrt(n))+1):
    while n%i==0:
        a.append(n//i)
        n=n//i
        

if a[-1]!=1:
    a.append(1)
for i in range(len(a)-1):
    print(a[i],end=' ')
print(a[-1])