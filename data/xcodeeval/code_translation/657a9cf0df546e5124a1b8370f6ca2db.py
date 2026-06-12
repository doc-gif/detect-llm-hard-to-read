t = input()
l = []
for i in range(10):
	t1 = input()
	l.append(t1)
for i in range(10,90,10):
	for j in range(len(l)):
		if t[i-10:i] == l[j]:
			print(j,end="")
			break