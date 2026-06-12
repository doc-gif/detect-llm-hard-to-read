n=int(input(''))
num=list(input(''))
lis=[]
count=0
for i in range(0,n):
    if num[i]=='1':
        count+=1
    else:
        lis.append(str(count))
        count=0
       # print('appended')
if num[n-1]=='1':
    lis.append(str(count))
else:
    lis.append(str(0))

print(''.join(lis))