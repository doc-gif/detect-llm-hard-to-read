n=int(input())
l=list(input())
a=l[0:n]
b=l[n:2*n]
a.sort()
b.sort()
count1=True
count2=True
flag=0
for i in range(n):
  if a[i]>b[i]:
    count1=False
  else:
    count2=False
  if (count1==False and count2==False) or (a[i]==b[i]):
    print('NO')
    flag=1
    break
if flag==0:
  print('YES')
  