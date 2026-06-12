Copy
n,k = input().split()
n = int(n)
k = int(k)
temp = 1
 
def lcm(x, y):
	if x>y:
		greater = x
	else:
		greater = y
	while True:
		if((greater%x==0)and(greater%y==0)):
			lcm = greater
			break
		greater+=1
	return lcm
 
def gcd(x,y):
	if x<y:
		temp = x
		x = y
		y = temp
	while(y):
		x, y = y,x%y
	return x 
 
if k == 0:
	print (n)
else:
	while k>0:
		temp=temp*10
		k=k-1
	x = gcd(temp,n)
	temp = int((temp * n)/x) 
	print (temp)