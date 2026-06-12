N = int(input())

# 初始化
matrix = [[0] * N] * N
for i in range(N):
    matrix[0][i] = 1
    matrix[i][0] = 1

for i in range(1, N):
    for j in range(1, N):
        matrix[i][j] = matrix[i-1][j] + matrix[i][j-1]

print(matrix[N-1][N-1])