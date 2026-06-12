import sys
input = sys.stdin.readline

def the_sieve_of_eratosthenes(n):
    s = [1] * (n + 1)
    x = []
    for i in range(2, n + 1):
        if s[i]:
            x.append(i)
            for j in range(i, n + 1, i):
                s[j] = 0
    return x

n, m = map(int, input().split())
x = the_sieve_of_eratosthenes(100)
ans = 1
pow2 = [1]
for _ in range(20):
    pow2.append(2 * pow2[-1])
for i in range(2, n + 1):
    y = []
    for j in x:
        if pow(i, j) > n:
            break
        y.append(j)
    ans0 = m
    for j in range(1, pow2[len(y)]):
        s = 1
        for k in range(len(y)):
            if j & pow2[k]:
                s *= y[k]
            if s > m:
                break
        c = 2 * ((bin(j).count("1") % 2) ^ 1) - 1
        ans0 += m // s * c
    ans += ans0
print(ans)