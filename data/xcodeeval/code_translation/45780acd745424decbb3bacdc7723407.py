R=lambda : map(int,input().split())
n,k=R()
print([(k+n-1)//n,1][n>k])





