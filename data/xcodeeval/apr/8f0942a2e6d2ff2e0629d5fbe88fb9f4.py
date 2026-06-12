a,b=map(int,input().split())
from collections import defaultdict
from math import gcd
a,b=min(a,b),max(a,b)
if b%a==0:
    print(0)
else:
    d=b-a
    d1=defaultdict(int)
    l=[]
    for i in range(1,d+1):
        if i**2<=d:
            if d%i==0:
                if i!=d//i:
                    l.append(i)
                    l.append(d//i)
                else:
                    l.append(i)
    ans=1000000000000000000
    for i in l:
        x=a//i
        if a%i!=0:
            x+=1
        y=x*i-a
        if (b+y)%(a+y)==0:
            ans=min(ans,b+y)
            z=b+y
            if d1[z]!=0:
                d1[z]=min(y,d1[z])
            else:
                d1[z]=y
    x=a//d
    if a%d!=0:
        x+=1
    k=x*d-a
    lcm=((a+k)*(b+k))//gcd(a+k,b+k)
    if lcm<ans:
        print(k)
    elif lcm>ans:
        print(d1[ans])
    else:
        print(min(k,d1[ans]))
        
        
        
    
