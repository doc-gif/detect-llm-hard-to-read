n,k=map(int,input().split())
a=list(map(int,input().split()))
c=0
d=0
for i in range(len(a)):
	if(a[i]>k):
		break
	else:
		c=c+1
if(c!=n):	
	for i in range(len(a)):
		if(a[n-i-1]>k):
			break
		else:
			d=d+1
		
print(c+d)

		