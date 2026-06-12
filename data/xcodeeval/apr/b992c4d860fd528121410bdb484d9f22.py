import sys
input = sys.stdin.readline

n,k=map(int,input().split())
mod=10**9+7

FACT=[1]
for i in range(1,2*10**5+1):
    FACT.append(FACT[-1]*i%mod)

FACT_INV=[pow(FACT[-1],mod-2,mod)]
for i in range(2*10**5,0,-1):
    FACT_INV.append(FACT_INV[-1]*i%mod)

FACT_INV.reverse()

def Combi(a,b):
    if 0<=b<=a:
        return FACT[a]*FACT_INV[b]*FACT_INV[a-b]%mod
    else:
        return 0

DP=[0]*(n+1)
DP[0]=1

for yoko in range(n):
    NDP=[0]*(n+1)
    for i in range(n+1):
        for j in range(max(1,i),n+1):
            PLUS=pow(k,i,mod)*Combi(n-i,j-i)*pow(k-1,n-j,mod)
            if i==j:
                PLUS-=pow(k-1,n,mod)

            #print(i,j,PLUS)
            NDP[j]=NDP[j]+DP[i]*PLUS

            NDP[j]%=mod

    DP=NDP
    #print(DP)

print(DP[-1])
            
        
        
        
