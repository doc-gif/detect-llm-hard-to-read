x1,y1,x2,y2=map(int,input().split())
x,y=map(int,input().split())
del_a=abs(x1-x2)
del_b=abs(y1-y2) 
if x==0:
    print('YES' if del_b%y==0 else 'NO')
    exit() 
if y==0:
    print('YES' if del_a%x==0 else 'NO')
    exit()
print ('YES' if (del_a%x==0 and del_b%y==0 and del_a//x%2==del_b//y%2) else 'NO')