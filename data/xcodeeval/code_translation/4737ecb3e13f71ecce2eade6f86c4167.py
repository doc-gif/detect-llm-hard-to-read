n=int(input())
s=input()
ans,i,k='',0,1
while i<n:
    ans+=s[i]
    i,k=i+k,k+1
print(ans)
