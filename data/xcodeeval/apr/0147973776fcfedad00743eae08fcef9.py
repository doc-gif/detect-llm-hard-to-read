import sys
def input(): return sys.stdin.readline().strip()


n, mod = map(int, input().split())

le = 500


def pow(x, y):  # x**y の mod を返す。modは素数でなくてもよい。
    ans = 1
    while y > 0:
        if y % 2 == 1:
            ans = (ans * x) % mod
        x = (x**2) % mod
        y //= 2
    return ans


def inv(x):  # x の mod での逆元を返す。modが素数で、xとmodが互いに素である必要あり。
    return pow(x, mod-2)


M = [1]  # i!のmod
mul = 1
for i in range(1, le):
    mul = (mul * i) % mod
    M.append(mul)

MI = [0] * (le-1) + [inv(M[le-1])]  # i!の逆元
for i in range(le-2, -1, -1):
    MI[i] = MI[i+1] * (i+1) % mod


def C(x, y):  # コンビネーション（組合せ）
    if y < 0 or y > x:
        return 0
    elif x > le:  # O(min(y, x-y))
        y = min(y, x-y)
        ans = 1
        for i in range(x, x-y, -1):
            ans = (ans * i) % mod
        return (ans * MI[y]) % mod
    else:  # O(1)
        ans = M[x]
        ans = (ans * MI[y]) % mod
        return (ans * MI[x-y]) % mod


M2 = [1]
for i in range(n+10):
    M2.append((M2[-1]*2) % mod)

CO = [[0] * (n+10) for i in range(n+10)]
for i in range(n+10):
    for j in range(n+10):
        CO[i][j] = C(i, j)

D = [[0] * (n+1) for i in range(n+2)]
# D[何個目まで見たか][そのうち手動ONの個数] = (見たうちの最右が自動ONである場合のパターン数)

D[0][0] = 1
for i in range(n+2):
    for j in range(n+1):
        for k in range(1, n+1):
            ind0 = i+k+1
            ind1 = j+k
            if ind0 <= n+1 and ind1 <= n:
                D[ind0][ind1] += D[i][j] * CO[j+k][k] * M2[k-1]
                D[ind0][ind1] %= mod
            if ind1 == n:
                break
        if ind0 == n+1:
            break

# print(D)
print(sum(D[-1]) % mod)
