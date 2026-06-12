n, m = map(int, input().split())
grid = [None for _ in range(n)]
for i in range(n):
	grid[i] = list(input())
pos = []
for i in range(n):
	for j in range(m):
		if grid[i][j] == 'W':
			pos.append((i, j))
ln = len(pos)

memo = {}
def solve(x, magic):
	if (x, magic) not in memo:
		if x >= ln:
			return 0

		res = solve(x + 1, magic)
		i, j = pos[x]

		if j > 0 and grid[i][j - 1] == 'P':
			grid[i][j - 1] = '.'
			res = max(res, 1 + solve(x + 1, magic + i * n + (j - 1) * m))
			grid[i][j - 1] = 'P'

		if i > 0 and grid[i - 1][j] == 'P':
			grid[i - 1][j] = '.'
			res = max(res, 1 + solve(x + 1, magic + (i - 1) * n + j * m))
			grid[i - 1][j] = 'P'

		if i < n - 1 and grid[i + 1][j] == 'P':
			grid[i + 1][j] = '.'
			res = max(res, 1 + solve(x + 1, magic + (i + 1) * n + j * m))
			grid[i + 1][j] = 'P'

		if j < m - 1 and grid[i][j + 1] == 'P':
			grid[i][j + 1] = '.'
			res = max(res, 1 + solve(x + 1, magic + (i + 1) * n + j * m))
			grid[i][j + 1] = 'P'

		memo[x] = res
		return res
	else:
		return memo[x]

print(solve(0, 0))
