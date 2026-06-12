n=int(input())
l=list(map(int,input().split()))
h=max(l)
m=min(l)
p1=l.index(h)+1
p2=l.index(m)+1
t=abs(p1-p2)
t1=abs(p1-n)
t2=abs(p2-n)
t3=abs(1-p2)
t4=abs(1-p1)

print(max(t,t1,t2,t3,t4))
