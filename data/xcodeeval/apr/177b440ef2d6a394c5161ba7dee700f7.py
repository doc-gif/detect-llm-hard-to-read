n = int(input())
sz = len(str(n))
def get(x):
    ans = 0
    nw = 1
    x1 = x
    for i in range(sz):
        x = x1
        if x < nw:
            while x < nw: x *= 10
            x -= 1 #тк сука [1;x)
        else:
            while x >= nw * 10: x //= 10
        x = min(x, n)
        ans += x - nw + 1
        nw *= 10
    return ans


MOD = 998244353

ans = 0
i = 1
while i <= n:
    l = i
    r = min(n, 10 ** (len(str(i))) - 1) + 1
    nw = (get(i) - i) // MOD
    while r - l > 1:
        mid = (l + r) // 2
        x = (get(mid) - mid) // MOD
        if nw == x:
            l = mid
        else:
            r = mid
    ans += nw * (r - i)
    # i += 1
    i = r
print(ans * -MOD)
