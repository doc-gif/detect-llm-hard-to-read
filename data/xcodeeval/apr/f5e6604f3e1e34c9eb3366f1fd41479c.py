n=int(input())*2
s=input()
d=dict()
aux=''
for i in range(len(s)):
    if s[i]=='(':
        d.update({(i,1):i+1})
        x=aux+')'
        for j in range(1,i+2):
            if x[j::] ==s[0:len(x)-j]:
                d.update({(len(aux),0):len(x[j::])})
                break
    else:
        d.update({(i,0):i+1})
        x=aux+'('
        for j in range(1,i+2):
            if x[j::]  ==s[0:len(x)-j]:
                d.update({(len(aux),1):len(x[j::])})
                break
    aux+=s[i]
d.update({(len(s),1):len(s)})
d.update({(len(s),0):len(s)})
dp=[[[0 for i in range(len(s)+1)] for j in range(n//2+1)] for k in range(n+1)]
dp[0][0][0]=1
mod=10**9+7
for i in range(n):
    for j in range(1,(n//2)+1):
        for k in range(len(s)+1):
            dp[i+1][j-1][d[(k,0)]]=(dp[i][j][k]+dp[i+1][j-1][d[(k,0)]])%mod
    for j in range(n//2):
        for k in range(len(s)+1):
            dp[i+1][j+1][d[(k,1)]]=(dp[i][j][k]+dp[i+1][j+1][d[(k,1)]])%mod
print(dp[n][0][len(s)]%mod)
