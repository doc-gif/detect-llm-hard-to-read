n = list(map(int,input().split()))
if(n[1] == 1):
	print(n[0]-1)
else:
	print(n[0]*(n[1]-1))