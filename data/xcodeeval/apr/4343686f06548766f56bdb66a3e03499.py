import math
n=int(input())
s=str(n)
di={}
#di={str(i):0 for i in range(0,10)}
for c in list(s):
    if c in di:
        di[c]+=1
    else:
        di[c]=1
#print(di)
    
v=[k for k in di]
cnt={k:1 for k in di}
ans=0
def solve():
    n=len(v)
    r=0
    if '0' in cnt:
        r=cnt['0']
    ans=n-r
    for i in range(1,n):
        ans=ans*(n-i)
    for k in cnt:
        ans=ans/(math.factorial(cnt[k]))
    #print(v,ans)
    return ans
def f():
    #print(v)
    global ans
    ans+=solve()
    for k in di:
        if cnt[k]<di[k]:
            v.append(k)
            cnt[k]+=1
            f()
            v.pop()
            cnt[k]-=1
            
f()
print(int(ans))
