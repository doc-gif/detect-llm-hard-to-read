p=input()
i=0
r=""
c=0
while (i<len(p)):
  if(p[i]!="/"):
    r=r+p[i]
    c=0
  elif(p[i]=="/" and c==0):
    r=r+"/"
    c=1
  i=i+1  
if(r[len(r)-1]=="/" and len(r)>1):
   r=r[0:(len(r)-1)]
print(r)    
