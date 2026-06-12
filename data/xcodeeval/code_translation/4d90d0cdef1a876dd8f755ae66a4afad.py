m=int(input())
s=input()+'0'
num=[]
le=len(s)
co=1
for i in range(le-1):
    if s[i]!=s[i+1]:
        num.append([ord(s[i]),co])
        co=1
    else:
        co+=1
li=len(num)
mi=min(num)
i2=mi[0]
for l in range(li):
    ma=max(num)
    i1=num.index(ma)
    le=len(num)
    if le<2 or i2==ma[0]:
        break
    elif i1==0:
        if num[i1][0]==num[i1+1][0]+1:
            num.remove(ma)
        else:
            num[i1][0]-=90
    elif i1==le-1:
        if num[i1][0]==num[i1-1][0]+1:
            num.remove(ma)
        else:
            num[i1][0]-=90
    elif num[i1][0]==num[i1+1][0]+1 or num[i1][0]==num[i1-1][0]+1:
         num.remove(ma)
    else:
        num[i1][0]-=90
    numd=[]
    num.append([1,0])
    lc=len(num)
    for i in range(lc-1):
        if num[i][0]==num[i+1][0]:
            num[i][1]=num[i][1]+num[i+1][1]
            num[i+1]=num[i]
        else:
            numd.append(num[i])
    num=numd[:]
to=0
for i in num:
    to+=i[1]
print(m-to)
