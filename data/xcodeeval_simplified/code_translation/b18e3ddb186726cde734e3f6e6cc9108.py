def yoba(a, k):
    if not a:
        return []
    if not k:
        return a
    m = max(a[: k + 1])
    mi = a.index(m)
    if m > a[0]:
        a[1 : mi + 1] = a[:mi]
        a[0] = m
        k -= mi
    return [a[0]] + yoba(a[1:], k)
a, k = input().split()
k = int(k)
print("".join(yoba(list(a), k)))