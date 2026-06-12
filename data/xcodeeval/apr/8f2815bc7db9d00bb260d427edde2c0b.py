s1=raw_input()
n=len(s1)
s2=raw_input()
m=len(s2)
if '?' not in s1 and '?' not in s2:
    sm1=0 
    sm2=0 
    for i in s1:
        if i=='+':sm1+=1 
        else: sm1-=1 
        
    for i in s2:
        if i=='+': sm2+=1 
        else: sm2-=1 
    print(1 if sm1==sm2 else 0)
    exit()
sm1=0 
for i in s1:
    if i=='+':sm1+=1 
    else: sm1-=1 
#make1=[s1]
make2=[s2]
ans=[]
while any('?'  in i for i in make2):
    n=[]
    for i in make2:
        if '?' not in i:
            ans.append(i)
        for j in range(len(i)):
            if i[j]=='?':
                n.append(i[0:j]+"-"+i[j+1:])
                n.append(i[0:j]+'+'+i[j+1:])
    make2=n
    #print(make2)
#make2=ans
make2=[i for i in make2 if '?' not in make2]
#print(make2)
#make2=list(set(make2))
#print(make2)
def sum_now(s):
    sum=0 
    for i in s:
        if i=='+': sum+=1 
        else: sum-=1 
    return sum 
make2=[sum_now(i) for i in make2]
#print(make2)
print(sum(i==sm1 for i in make2)*(1.0)/len(make2))