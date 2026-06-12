n=int(input())
lookup={}
for i in range(n):
    x=list(map(int,input().split()))
    for j in range(n):
        lookup[x[j]]=(i,j)
bestrook=[0,0]
bestbish=[0,0]
bestknight=[0,0]
for i in range(1,n**2):
    x=abs(lookup[i][0]-lookup[i+1][0])
    y=abs(lookup[i][1]-lookup[i+1][1])
    if x==0 or y==0:
        bestrook[0]+=1
    else:
        bestrook[0]+=2
    if x==y:
        bestbish[0]+=1
    elif (x-y)%2==0:
        bestbish[0]+=2
    else:
        bestbish[0]+=1000
    if {x,y}=={1,2}:
        bestknight[0]+=1
    elif x**2+y**2 in [4,16,20,10,18]:
        bestknight[0]+=2
    elif x**2+y**2==2 and lookup[i] not in [(0,0),(n-1,0),(0,n-1),(n-1,n-1)] and lookup[i+1] not in [(0,0),(n-1,0),(0,n-1),(n-1,n-1)]:
        bestknight[0]+=2
    elif {x,y} in [{5,0},{3,0},{1,0},{6,1},{4,1},{5,2},{3,2},{6,3},{4,3},{5,4}]:
        bestknight[0]+=3
    else:
        bestknight[0]+=1000
    bestrook[0]=min(bestrook[0],bestbish[0]+1,bestknight[0]+1)
    bestbish[0]=min(bestrook[0]+1,bestbish[0],bestknight[0]+1)
    bestknight[0]=min(bestrook[0]+1,bestbish[0]+1,bestknight[0])
best=(bestrook[0],bestbish[0],bestknight[0])
if min(best)==best[0]:
    print(bestrook[0],bestrook[1])
elif min(best)==best[1]:
    print(bestbish[0],bestbish[1])
else:
    print(bestknight[0],bestknight[1])