def solve(str,n,k):
    g=str.index('G')
    t=str.index('T')
    if g>t:
        for i in range(t,g+1,k):
            if str[i]=='G':
                return True
            if str[i]=='#':
                return False
    else:
        for i in range(g,t+1,k):
            if str[i]=='T':
                return True
            if str[i]=='#':
                return False
    return False
            

strnk=(input())
str1=strnk.split(" ")
n=int(str1[0])
k=int(str1[1])
str=input()
if solve(str,n,k)==True:
    print("YES")
else:
    print("NO")
