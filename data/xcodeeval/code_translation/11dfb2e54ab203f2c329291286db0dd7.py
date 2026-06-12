def sc(i,j,k):
   xx=0
   for t in range(5):
      xx+=(m[i][t]-m[j][t])*(m[i][t]-m[k][t])
   return xx
n= int(input())

m=[]
mm=n
ans=[]
if (n > 36):
   print("0")
else:
   for i in range(n):
      ans.append(1)
      a,b,c,d,e=map(int,input().split())
      m.append([a,b,c,d,e])
   for i in range(n):
      for j in range(n):
         if (i != j):
            for k in range(n):
               if (i != k) and ( j != k):
                  if sc(i,j,k) >0:
                     ans[i]=-1
   for i in range(n):
      if ans[i]==-1:
         mm+=-1
   print(mm)
   for i in range(n):
      if ans[i]==1:
         print(i+1)