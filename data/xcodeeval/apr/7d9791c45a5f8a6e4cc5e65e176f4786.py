from math import factorial
MOD = 10**9+7

def binom(n, k):
    if k > n-k: return binom(n, n-k)
    res = 1
    for i in range(k): res = res*(n-i)//(i+1)
    return res

def comp_ones_vecs(k, n):
    # k ones, n vectors
    if k < n: return 0
    ans = 0
    for Z in range(n):
        ans+= (-1)**Z * binom(n,Z) * (n-Z)**k
    return ans // factorial(n)

def comp_ones_frees_vecs(k, f, n):
    # k prefixed ones, f digits of freedom, n vectors
    ans = 0
    for i in range(f+1):
        ans+= comp_ones_vecs(k+i, n) * binom(f, i)
    return ans

def comp_ones_frees(k, f):
    # k prefixed ones, f digits of freedom
    ans = 0
    for n in range(1, k+f+1):
        ans+= comp_ones_frees_vecs(k, f, n)
    return ans

k = int(input())
bink = list(map(int, bin(k)[2:]))
ans = 1 + comp_ones_frees(sum(bink), 0)
ones = 0
for i in range(len(bink)):
    if bink[i] == 0: continue
    ans+= comp_ones_frees(ones, len(bink)-i-1)
    ones+= 1
print(ans % MOD)