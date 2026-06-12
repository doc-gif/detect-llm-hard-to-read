def main():
	n = list(map(int, input().strip().split()))
	n, m = tuple(n)
	temp = 1
	while m != n:
		if m % 10 == 0:
			print(0)
			return
		temp *= m
		m -= 1
	print(temp % 10)
	
main()