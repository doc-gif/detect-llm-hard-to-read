r1,r2=map(int,input().split())
c1,c2=map(int,input().split())
d1,d2=map(int,input().split())		
a=(r1+c1-d2)//2
b=c1-a
c=r1-a
d=d1-a
l={a,b,c,d}
if len(l)<4 or min(l)<1 or max(l)>9 or b+d!=r2 or a+d!=d1 or c+d!=c2:
	print(-1)
else:
	print(a,c)
	print(b,d)