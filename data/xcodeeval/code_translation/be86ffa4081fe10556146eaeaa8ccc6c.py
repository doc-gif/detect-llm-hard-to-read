n,b = map(int,input().split())
l = list(map(int,input().split()))
ce,co=0,0
c = 0
s = 0
ans = 0
z = []
for i in range(n):
    if(l[i]%2):
        co+=1
    else:
        ce+=1
    if(ce==co):
        if(i<n-1):
            z.append(abs(l[i+1]-l[i]))
            ce,co=0,0
z.sort()
for i in z:
    ans+=1
    s+=i
    if(s>b):
        ans-=1
        print(ans)
        exit(0)
print(ans)