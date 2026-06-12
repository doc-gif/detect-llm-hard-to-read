q=input()
v=''
w=[]
for i in range(0,len(q),2):
    w.append(int(q[i]))
w.sort()
for i in range(len(w)):
    if i==len(w)-1:
        v=v+str(w[i])
    elif i==0:
        v=str(w[i])+'+'
    else:
        v=v+str(w[i])+'+'
print(v)