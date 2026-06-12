MOD = 998244353

n, k = map(int, input().split())
f = [0] * (5 * n + 5)
for d in map(int, input().split()):
    f[d] = 1

def ntt_transform(a, P, G, inv=False):
    n, k = 1, 0
    while n < len(a):
        k += 1
        n *= 2
    a += [0] * (n - len(a))
    
    n2 = n // 2
    w = [1] * n2
    w[1] = pow(G, (P - 1) // n, P)
    if inv: w[1] = pow(w[1], P - 2, P)
    for i in range(2, n2):
        w[i] = w[i - 1] * w[1] % P

    rev = [0] * n
    for i in range(n):
        rev[i] = rev[i >> 1] >> 1
        if i & 1: rev[i] |= n2
        if i < rev[i]: a[i], a[rev[i]] = a[rev[i]], a[i]

    l = 2
    while l <= n:
        half, diff = l // 2, n // l
        for i in range(0, n, l):
            pw = 0
            for j in range(i, i + half):
                v = a[j + half] * w[pw] % P;
                a[j + half] = a[j] - v if a[j] - v >= 0 else a[j] - v + P
                a[j] = a[j] + v if a[j] + v < P else a[j] + v - P
                pw += diff
        l *= 2

    if inv:
        inv_n = pow(n, P - 2, P)
        for i in range(n): a[i] = a[i] * inv_n % P;


ntt_transform(f, MOD, 3)
f = [pow(x, n // 2, MOD) for x in f]
ntt_transform(f, MOD, 3, inv=True)

ans = sum(x * x % MOD for x in f) % MOD
print(ans)
