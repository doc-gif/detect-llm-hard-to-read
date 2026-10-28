na=int(input())#----->
a=list(input().lower())
a.sort()
d=[]
for i in range(97,123):
    d.append(chr(i))
f=[]
c=1
for i in a:
    if i not in f:
         f.append(i)
         c+=1
    if c==27:
        break

if f==d :
    print("YES")
else:
    print("NO")











    





    
