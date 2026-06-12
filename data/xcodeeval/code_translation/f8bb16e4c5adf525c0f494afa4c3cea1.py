n,m,s=[int(s) for s in input().split()]
a=(n % s)
b=(m % s)
if a==0 and n>=s:a=s
if b==0 and m>=s:b=s
unit=(a*b)

print(((n-1)//s+1)*((m-1)//s+1)*unit)
