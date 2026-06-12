s = str(input())
s1 = sorted(s)
ac1 = 0
for i in s:
	if i == 'a':
		ac1 += 1
leng = len(s1) / 2
if ac1 > leng:
    print(len(s1))
else:
    while ac1 <= leng:
    	s1.pop(-1)
    	leng = len(s1) / 2
    print(len(s1))