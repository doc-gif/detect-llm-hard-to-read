import sys
range = xrange
input = raw_input

MOD = 10**9+7
def mult(A,B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            for z in range(n):
                C[x][y] += A[z][y]*B[x][z]
            C[x][y]%=MOD
    return C

def vecmult(A,B):
    n = len(A)
    C = [0]*n
    for y in range(n):
        C[y] = sum(A[x][y]*B[x] for x in range(n))%MOD
    return C

n,m = [int(x) for x in input().split()]


#def DP(n):
#    if n<=0:
#        return 1 if n==0 else 0
#    else:
#        return DP(n-m) + DP(n-1)


mapper = [[0]*m for _ in range(m)]

mapper[0][0] = 1
mapper[-1][0] = 1
for i in range(m-1):
    mapper[i][i+1] = 1

def power(A,B,m):
    n = len(A)
    if m == 0:
        return B
    while m>1:
        if m%2==1:
            B = vecmult(A,B)
        A = mult(A,A)
        m//=2
    return vecmult(A,B)

vec = [1]*m
vec = power(mapper,vec,n)
print(vec[-1]%MOD)
