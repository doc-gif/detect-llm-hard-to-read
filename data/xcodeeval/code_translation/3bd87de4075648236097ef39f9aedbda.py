def q92a():
	n, m = tuple([int(num) for num in input().split()])
	n_cycle = n * (n+1) // 2
	m = m % n_cycle
	for i in range(n):
		if(m >= i):
			m -= i
		else:
			break
	print(m)
 
q92a()