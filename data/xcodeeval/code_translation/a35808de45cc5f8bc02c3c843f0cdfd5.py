n,p,k=input().split()
n=int(n)
p=int(p)
k=int(k)
s=p+k
t=p-k
if s>=n and t<=1:
	for i in range(1,p,1):
		print(i,end=' ')
	print('(',end='')
	print(p,end='')
	print(')',end=' ')
	for i in range(p+1,n+1,1):
		print(i,end=' ')
if s>=n and t>1:
	print('<<',end=' ')
	for i in range(t,p,1):
		print(i,end=' ')
	print('(',end='')
	print(p,end='')
	print(')',end=' ')
	for i in range(p+1,n+1,1):
		print(i,end=' ')
if s<n and t<=1:
	for i in range(1,p,1):
		print(i,end=' ')
	print('(',end='')
	print(p,end='')
	print(')',end=' ')
	for i in range(p+1,s+1,1):
		print(i,end=' ')
	print('>>',end=' ')
if s<n and t>1:
	print('<<',end=' ')
	for i in range(p-k,p,1):
		print(i,end=' ')
	print('(',end='')
	print(p,end='')
	print(')',end=' ')
	for i in range(p+1,s+1,1):
		print(i,end=' ')
	print('>>',end=' ')