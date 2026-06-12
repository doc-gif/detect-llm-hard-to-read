n, m, a = map(int, input().split())

if n%a == 0:
	nn = int(n / a)
else:
	nn = int(n / a) + 1

if m%a == 0:
	mm = int(m / a)
else:
	mm = int(m / a) + 1

print(nn * mm)