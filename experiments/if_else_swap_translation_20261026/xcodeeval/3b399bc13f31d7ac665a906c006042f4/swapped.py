n, m, k = map(int, input().split())
if not (k <= n - 1):
    k = k - n
    if (n - k // (m - 1)) % 2 == 0:
        print((n - k // (m - 1)), 2 + k % (m - 1))
    else:
        print((n - k // (m - 1)), m - k % (m - 1))
else:
    print(1 + k, 1)
        