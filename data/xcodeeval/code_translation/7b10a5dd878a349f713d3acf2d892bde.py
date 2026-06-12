n, m = [int(i) for i in input().split(" ")]
na = [int(i) for i in input().split(" ")]
ma = [int(i) for i in input().split(" ")]
intersection = set(na) & set(ma)
if len(intersection) != 0:
	print(min(intersection))
else:
	arr = set()
	for i in na:
		for j in ma:
			arr.add(i*10+j)
			arr.add(j*10+i)
	print(min(arr))