n,m=map(int,input().split())
x=min(n,m)
y=max(n,m)
count=0
for i in range(1,x+1):
    j=5-(i%5)
    count+=(y-j)//5
    count+=1
print(count)