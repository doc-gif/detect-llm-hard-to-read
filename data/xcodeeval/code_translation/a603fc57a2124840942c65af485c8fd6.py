b=list(map(int,input().split(':')))

n=int(input())
s=0
o=0
c=b[1]
g=n
if n==0:
    if b[0]<10:
        if b[1]<10:
            print('0'+str(b[0])+':'+'0'+str(b[1]))
        else:
            print('0' + str(b[0]) + ':' + str(b[1]))
    else:
        if b[1]<10:
            print(str(b[0])+':'+'0'+str(b[1]))
        else:

            print(str(b[0])+':'+str(b[1]))



if n%60==0 and g>0:
    b[0]+=n//60

elif n+b[1]>=60:
    s=60-b[1]
    g=n
    n=n-s
    o=n//60
    b[0]+=1+o
    b[1]=n-60*o
elif n+b[1]<60:
    b[1]=b[1]+n

if b[0]>=24 and g>0:
    
    a=b[0]//24
    b[0]=b[0]-24*a
    if b[0]<10:
        if b[1]<10:
            print('0'+str(b[0])+':'+'0'+str(b[1]))
        else:
            print('0' + str(b[0]) + ':' + str(b[1]))
    else:
        if b[1]<10:
            print(str(b[0])+':'+'0'+str(b[1]))
        else:

            print(str(b[0])+':'+str(b[1]))
elif g>0:

    if b[0]<10:
        if b[1]<10:
            print('0'+str(b[0])+':'+'0'+str(b[1]))
        else:
            print('0' + str(b[0]) + ':' + str(b[1]))
    elif g>0:
        if b[1]<10:
            print(str(b[0])+':'+'0'+str(b[1]))
        else:

            print(str(b[0])+':'+str(b[1]))
