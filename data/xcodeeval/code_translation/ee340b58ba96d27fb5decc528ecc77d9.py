r,g,f=map(int,input().split())
c=29
while(1):
    c=c+1
    if r>=2:
        r=r-2
    elif r==1:
        r=r-1
    
    if r==0 and g==0 and f==0:
        break
    c=c+1
    if g>=2:
        g=g-2
    elif g==1:
        g=g-1
    if r==0 and g==0 and f==0:
        break
    c=c+1
    if f>=2:
        f=f-2
    elif f==1:
        f=f-1
    if r<=0 and g<=0 and f<=0:
        break
print(c)
    
    
        
    