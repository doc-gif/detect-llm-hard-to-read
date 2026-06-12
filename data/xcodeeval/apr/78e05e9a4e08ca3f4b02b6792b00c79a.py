n=int(input())
xx=[]
yy=[]
countx=[0 for i in range(51)]
county=[0 for i in range(51)]
for _ in range(4*n+1):
    x,y=map(int,input().split(' '))
    xx.append(x)
    yy.append(y)
    countx[x]+=1
    county[y]+=1
xxx=[]
yyy=[]
for i in range(50):
    if countx[i]>=2:
        xxx.append(i)
    if county[i]>=2:
        yyy.append(i)
xmin=min(xxx)
xmax=max(xxx)
ymin=min(yyy)
ymax=max(yyy)
for i in range(4*n+1):
    if xx[i]==xmin or xx[i]==xmax:
        if  yy[i]<=ymax and yy[i]>=ymin:
            continue
    if yy[i]==ymin or yy[i]==ymax:
        if  xx[i]<=xmax or xx[i]>=xmin:
            continue
    index=i
print(xx[index],yy[index])