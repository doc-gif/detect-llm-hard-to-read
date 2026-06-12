import sys
input = sys.stdin.readline

n,m=map(int,input().split())

S=[i for i in range(n+1)]

for i in range(2,n+1):
    if S[i]==i:
        for j in range(i,n+1,i):
            if S[j]==j:
                S[j]=i

def fact(x):
    P=[]
    while x!=1:
        P.append(S[x])
        x//=S[x]

    NOW={1}
    for p in P:
        NOW|={n*p for n in NOW}

    return NOW

DP=[0]*(n+1)

DP[1]=1
DP[2]=2
DP[3]=5
#DP[4]=12
#DP[5]=25

for i in range(4,n+1):
    SU=DP[i-1]*2+1
    
    for f in fact(i):
        if f==1 or f==i:
            continue
        SU+=DP[i//f]-DP[(i-1)//f]

    DP[i]=SU%m

print(DP[n])
    
    
