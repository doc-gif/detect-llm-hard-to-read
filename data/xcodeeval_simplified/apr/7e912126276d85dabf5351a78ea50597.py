import sys

range = xrange
input = raw_input
MOD = 10**9 + 7


def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            for z in range(n):
                C[x][y] += A[z][y] * B[x][z]
            C[x][y] %= MOD
    return C


def matrix_vector_multiply(A, v):
    n = len(A)
    result = [0] * n
    for y in range(n):
        result[y] = sum(A[x][y] * v[x] for x in range(n)) % MOD
    return result


n, m = map(int, input().split())
mapper = [[0] * m for _ in range(m)]
mapper[0][0] = 1
mapper[-1][0] = 1
for i in range(m - 1):
    mapper[i][i + 1] = 1


def power_matrix_vector(A, v, exponent):
    if exponent == 0:
        return v
    while exponent > 1:
        if exponent % 2 == 1:
            v = matrix_vector_multiply(A, v)
        A = matrix_multiply(A, A)
        exponent //= 2
    return matrix_vector_multiply(A, v)


initial_vector = [1] * m
result_vector = power_matrix_vector(mapper, initial_vector, n)
print(result_vector[-1] % MOD)
