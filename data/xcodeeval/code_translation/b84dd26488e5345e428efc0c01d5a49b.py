n,m = map(int,input().split())
p = 10**9+7
print(pow((pow(2,m,p)-1),n,p))
