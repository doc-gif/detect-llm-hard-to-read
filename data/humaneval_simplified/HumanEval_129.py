from typing import *


def minPath(grid, k):
    n = len(grid)
    val = n * n + 1
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                neighbors = []
                if i > 0:
                    neighbors.append(grid[i - 1][j])
                if j > 0:
                    neighbors.append(grid[i][j - 1])
                if i < n - 1:
                    neighbors.append(grid[i + 1][j])
                if j < n - 1:
                    neighbors.append(grid[i][j + 1])
                if neighbors:
                    val = min(neighbors)
    ans = [1 if i % 2 == 0 else val for i in range(k)]
    return ans
