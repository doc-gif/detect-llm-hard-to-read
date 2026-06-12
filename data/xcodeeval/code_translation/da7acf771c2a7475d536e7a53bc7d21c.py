n, k = map(int, input().split())

if n // 2 < k:
	print(0, 0, n)
else:
	a = n // 2 // (k + 1)
	b = n // 2 // (k + 1) * k
	print(a, b, n - a - b)
