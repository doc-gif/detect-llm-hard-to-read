MOD = int(1e9 + 7)


def mult(l, r):
    return (l * r) % MOD


def fast_exp(b, e):
    if e == 0:
        return 1
    if e % 2 == 1:
        return mult(b, fast_exp(b, e - 1))
    else:
        b2 = fast_exp(b, e // 2)
        return mult(b2, b2)


n, k = map(int, input().split())
print(n, k)
fact = [1] * (n + 1)
for i in range(1, n + 1):
    fact[i] = mult(i, fact[i - 1])
ifact = [1] * (n + 1)
ifact[n] = fast_exp(fact[n], MOD - 2)
for i in range(n - 1, 0, -1):
    ifact[i] = mult(i + 1, ifact[i + 1])


def binom(N, K):
    return mult(mult(fact[N], ifact[K]), ifact[N - K])


def get(i, j):
    X = i * j
    Y = (n - i) * j
    Z = (n - j) * i
    tot = X + Y + Z
    sign = 1 if (i + j) % 2 == 0 else MOD - 1
    ans = mult(sign, binom(n, j))
    ans = mult(ans, binom(n, i))
    ans = mult(ans, fast_exp(k, n * n - tot))
    ans = mult(ans, fast_exp(k - 1, tot))
    return ans


ans = 0
for i in range(n + 1):
    for j in range(n + 1):
        ans = (ans + get(i, j)) % MOD
print(ans)
