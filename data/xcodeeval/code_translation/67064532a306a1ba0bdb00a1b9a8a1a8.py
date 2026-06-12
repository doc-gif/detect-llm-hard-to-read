def next(x):
    k = 0
    while (x > 1):
        x //= 2
        k += 1
    return k

def st(x):
    k = 1
    for i in range(x):
        k *= 2
    return k


n, b, p = map(int, input().split())
ans = 0
ll = n * p
while(n != 1):
    k = st(next(n))
    n -= k
    n += (k // 2)
    ans += (k // 2) * 2 * b
    ans += (k // 2)
print(ans)
print(ll)

# Wed Oct 07 2020 15:05:24 GMT+0300 (Москва, стандартное время)

# Thu Oct 08 2020 09:54:00 GMT+0300 (Москва, стандартное время)

# Thu Oct 08 2020 09:54:31 GMT+0300 (Москва, стандартное время)
