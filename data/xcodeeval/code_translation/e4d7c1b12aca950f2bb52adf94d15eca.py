s=input()
if len(s)<5:
	print("Too weak")
else:
	n=len(s)
	a=[]
	b=[]
	c=[]
	for i in range(n):
		if s[i].isupper():
			a.append(s[i])
		elif s[i].islower():
			b.append(s[i])
		elif s[i].isnumeric():
			c.append(s[i])
	if len(a)==0 or len(b)==0 or len(c)==0:
		print("Too weak")
	else:
		print("Correct")