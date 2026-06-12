### A. Contest for Robots

n=int(input())
a=[int(x) for x in input().split()]
b=[int(y) for y in input().split()]
A=B=t=0

for i in range(n):
    if a[i]>b[i]:
        A+=1
    elif a[i]<b[i]:
        B+=1
if A==0:
    print(-1)
else:
    print(B//A+1)