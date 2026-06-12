def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s


def binsearch(a, l, r, elem):
    medium = (l + r) // 2
    s = a[medium] - sum_digits(a[medium])
    s2 = a[medium + 1] - sum_digits(a[medium + 1])
    while not (s2 >= elem and s < elem):
        if s <= elem:
            l = medium
        elif s >= elem:
            r = medium
        k = medium
        medium = (l + r) // 2
        if k == medium:
            break
        s = a[medium] - sum_digits(a[medium])
        s2 = a[medium + 1] - sum_digits(a[medium + 1])
    s1 = a[medium - 1] - sum_digits(a[medium - 1])
    if s >= elem and s1 < elem:
        return medium
    elif s2 >= elem and s < elem:
        return medium + 1
    else:
        return len(a)


n, s = map(int, input().split())
a = [i for i in range(n + 1)]
y = binsearch(a, 0, len(a) - 1, s)
print(n - y + 1)
