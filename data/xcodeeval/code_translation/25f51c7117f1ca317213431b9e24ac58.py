def c(M,x,y):
 p=[-2,+2]
 q=[-1,+1]
 l=[M[x+p[i]][y+q[j]]!=0 for i in range(len(p)) for j in range(len(q)) if(0<=x+p[i]<8 and 0<=y+q[j]<8)]
 l+=[M[x+q[i]][y+p[j]]!=0 for i in range(len(q)) for j in range(len(p)) if(0<=x+q[i]<8 and 0<=y+p[j]<8)]
 return 1 in l 
mp=['a','b','c','d','e','f','g','h']
i=input
n=i()
m=i()
M=[[0 for x in range(8)]for y in range(8)]
l=[[mp.index(n[0]),int(n[1])-1],[mp.index(m[0]),int(m[1])-1]]
M[l[0][0]][l[0][1]]=2
M[l[1][0]][l[1][1]]=1
r=0
for x in range(8):
 for y in range(8):
  if(0==M[x][y]):
   if(x==l[0][0]or y==l[0][1]):continue
   if(c(M,x,y)==False):r+=1
print(r)
