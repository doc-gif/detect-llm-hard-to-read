import string
U = string.ascii_uppercase
k = string.ascii_lowercase
z = input()
t = input()
index1 = 0
index2 = 0
index3 = 0
index4 = 0
zz = []
tt = []
for i in z:
    if i in U:
        index1 = U.find(i)
        zz.append(index1)
        index1 = 0
    elif i in k:
        index2 = k.find(i)
        zz.append(index2)
        index2 = 0
for i in t:
    if i in U:
        index3 = U.find(i)
        tt.append(index3)
        index3 = 0
    elif i in k:
        index4 = k.find(i)
        tt.append(index4)
        index4 = 0
p = len(zz)
for i in range(p):
    if zz[i] == tt[i]:
        None
    elif zz[i] < tt[i]:
        w-=1
    elif zz[i] > tt[i]:
        w+=1
print(w)   