n,m=[int(x) for x in input().split()]
a=0
while n*m!=0:
    n=n-1
    m=m-1
    a+=1
if a%2==0:
    print('Malvika')
else:
    print('Akshat')
