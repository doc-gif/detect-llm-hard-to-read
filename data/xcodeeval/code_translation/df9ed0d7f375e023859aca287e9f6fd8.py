# your code goes here
n, m = map(int, input().split())
s = input()
l = []
for e in s:
	l.append(e)
	
l.sort()
a = []
a.append(l[0])
del l[0]
su = ord(a[0])-ord('a')+1
flag = 0
while len(a) < m:
	i = 0
	while ord(l[i])-ord('a')+1 < ord(a[-1])-ord('a')+3:
		if i == len(l)-1:
			print(-1)
			flag = 1
			break
		i+=1
	if flag == 1:
		break
	a.append(l[i])
	del l[i]
	su += ord(a[-1])-ord('a')+1
if not flag:
	print(su)

	
		

