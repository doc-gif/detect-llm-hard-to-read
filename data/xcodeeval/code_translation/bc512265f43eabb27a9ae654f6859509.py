def gcd(a,b):
    if(a%b==0):
        return b
    else:
        return gcd(b,a%b)

[t1,t2,x1,x2,t0]=input().split(' ')
#[t1,t2,x1,x2,t0]=[100,110,2,2,109]
t1=int(t1)
t2=int(t2)
x1=int(x1)
x2=int(x2)
t0=int(t0)

a=t2-t0
b=t0-t1

if(a==0 and b==0):
    print(x1,x2)
    exit(0)

if (a==0):
    y1=0
    y2=x2
    print(y1,y2)
    exit(0)
    
if (b==0):
    y1=x1
    y2=0
    print(y1,y2)
    exit(0)
    
g=gcd(a,b)
a=int(a/g)
b=int(b/g)
if(a<=x1 and b<=x2):
    mintime=int(x1/a)
    if(mintime>int(x2/b)):
        mintime=int(x2/b)
    print(mintime*a,mintime*b)
    exit(0)

y1=1
y2=1
miny1=1
miny2=1
minn=99999
fg=0
while(y1<=x1 and y2<=x2):
    if(y1/y2<a/b):
        if(minn>a/b-y1/y2):
            minn=a/b-y1/y2
            miny1=y1
            miny2=y2
            fg=1
        y1=y1+1
    else:
        y2=y2+1
y1=miny1
y2=miny2
mintime=int(x1/y1)
if(mintime>int(x2/y2)):
    mintime=int(x2/y2)
if(fg==1):
    print(mintime*y1,mintime*y2)
else:
    print(0,x2)




