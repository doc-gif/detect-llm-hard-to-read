from math import sqrt, ceil


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def count(p):
    return p * (3 * p + 2)


def bin_search(n):
    left = 0
    right = ceil(sqrt(n))
    while right - left > 1:
        mid = (left + right) // 2
        if count(mid) > n:
            right = mid - 1
        else:
            left = mid
    if count(right) > n:
        return left
    else:
        return right


def get_pos(n, p):
    if n < p:
        return add((p - 1, -2 * p + 2), (n, 2 * n))
    n -= p
    if n < p - 1:
        return add((1 + 2 * (p - 1), 2), (-n, 2 * n))
    n -= p - 1
    if n < p:
        return add((p, 2 * p), (-2 * n, 0))
    n -= p
    if n < p:
        return add((-p, 2 * p), (-n, -2 * n))
    n -= p
    if n < p:
        return add((-2 * p, 0), (n, -2 * n))
    raise RuntimeError("You're a big guy")


n = int(input())
if n == 0:
    print(0, 0)
else:
    p = bin_search(n)
    start = count(p)
    n -= start
    ans = get_pos(n, p + 1)
    print(ans[0], ans[1])
