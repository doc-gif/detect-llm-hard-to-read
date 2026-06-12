x=int(input())
di=[0,3,1,2]
di2=['D','A','C','B']
re=di[x%4]
imax=0
for i in range(1,3):
    if re<di[(x+i)%4]:
        imax=i
        re=di[(x+i)%4]
print(imax,di2[di.index(re)])
