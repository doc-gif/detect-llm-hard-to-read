L1,R1,L2,R2,K = map(int, input().split())
ans=0
L = max(L1,L2)
R = min(R1,R2)
if L<=R:
    ans=R-L+1
    if L<=K<=R:
        ans-=1
print(ans)
