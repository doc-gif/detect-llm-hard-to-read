aa = input().split()
n = int(aa[0])
k = int(aa[1])
a = input().split()


master = []
new = []
for i in range(1, n + 1):
	if i % k == 0:
		new.append(a[i - 1])
		master.append(new)
		new = []
	else:
		new.append(a[i-1])

def count(list, item):
	count = 0
	for c in list:
		if c == item:
			count += 1
	return count

def common(list):
	counts = []
	maxcount = 0
	for stuff in list:
		if count(list, stuff) >= maxcount:
			maxitem = stuff
			maxcount = count(list, stuff)
	return maxitem

check = True
for lists in master:
	if count(master, lists) > 1:
		check = False

answer = 0

if check ==True:
	reference = common(a)
	for i in a:
		if i != reference:
			answer += 1




if check == False:
	for i in master:
		ref = common(master)
		if i != ref:
			for j in range(len(i)):
				if i[j] != ref[j]:
					answer += 1
print(answer)