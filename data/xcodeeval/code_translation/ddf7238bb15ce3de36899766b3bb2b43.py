a = input()
ans = 0
b = a
for i in range(len(a)):
	if a == a[::-1]:
		b = a[i:]
		if b != b[::-1]:
			ans = len(a)-i
			break
	elif a != a[::-1]:
		ans = len(a)
	elif a[i]==a[i-1]:
		ans  = 0
print(ans)
