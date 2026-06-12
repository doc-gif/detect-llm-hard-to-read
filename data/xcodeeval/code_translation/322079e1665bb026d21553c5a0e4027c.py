n=int(input())
m=input()
a=0
b=0
for i in range(1,len(m)):
    if m[i]=='F' and m[i-1]=='S':
        a+=1
    elif m[i]=='S' and m[i-1]=='F':
        b+=1
if a>b:
    print('YES')
else:
    print('NO')