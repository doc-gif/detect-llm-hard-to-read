inp=input()
count=0
count2=0
for i in inp:
    if i=='4':
        count=count+1
    elif i=='7':
        count2=count2+1

if (count==4 or count==7) and count2==0:
    print('YES')
elif (count2==4 or count2==7) and count==0:
    print('YES')
elif count+count2==4 or count+count2==7:
    print('YES')
else:
    print('NO')
