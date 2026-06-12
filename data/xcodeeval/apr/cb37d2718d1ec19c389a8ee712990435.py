# N boxes can be filled with type H or type T objects
# 1 H object takes 1 box
# 1 H can turn into M T objects which must take contiguous boxes
# How many ways to fill N boxes?

# E.g. N=4, M=2 -> return 5: HHHH, HHTT, HTTH, TTHH, TTTT

# Constraints: N <= 10^18


def _solve(n, m, memo):
	if n <= 0: return 0
	if n < m: return 1
	if n == 1: return 2
	if (n, m) in memo: return memo[(n, m)]

	out = 0
	mid = n // 2

	# No M block hanging over 2 halves
	out += _solve(mid, m, memo) * _solve(n-mid, m, memo) % 1000000007 

	# M block over 2 halves
	for i in range(1,m):  # i = part of M block in first half
		if mid-i < 0 or n-mid+i-m < 0: continue
		n1 = 1 if mid-i == 0 else _solve(mid-i, m, memo)
		n2 = 1 if n-mid+i-m == 0 else _solve(n-mid+i-m, m, memo)
		out += n1*n2 

	memo[(n, m)] = out
	return out


def solve(n, m):
	return _solve(n, m, {})


def main():
	from sys import stdin

	n, m = list(map(int, stdin.readline().strip().split()))
	out = solve(n, m)
	print('{}'.format(out))


if __name__ == '__main__':
	main()
