input()
l=list(map(int,input().split()))
total=0
dic={}
for i in range(len(l)):
    for j in range(i+1,len(l)):
        if(l[j]>l[i]):
            temp=l[j]
            l[j]=l[i]
            l[i]=temp
for i in range(0,len(l)-1,2):
    total+=abs(l[i]-l[i+1])

print(str(total))

