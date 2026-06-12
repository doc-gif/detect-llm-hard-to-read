n,colors,cnt=int(input()),[int(x) for x in input().split()],0
while(len(colors) > 0):
    mini=min(colors)
    colors=[int(x) for x in colors if x%mini !=0]
    cnt+=1
print(cnt)