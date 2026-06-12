data = [int(info) for info in input().split(' ')]

mid = data[0]
ma = max(data)
mi = min(data)

for i in data:
	if i < ma and i > mi:
		mid = i

print((ma - mid) + (mid - mi))

