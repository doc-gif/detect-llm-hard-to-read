def binsearch(predicate, left, right):
    while left + 1 != right:
        mid = (left + right) // 2
        if predicate(mid):
            right = mid
        else:
            left = mid
    return right
n = int(input())
if n == 0:
    print(0, 0)
else:
    i = binsearch(lambda idx: n <= 3 * idx * (idx + 1), 0, 10**18)
    acc = 3 * (i - 1) * i
    j = binsearch(lambda idx: n <= acc + i * (idx + 1), -1, 6)
    k = n - acc - i * j - 1
    dy = [0, 2, 2, 0, -2, -2]
    dx = [2, 1, -1, -2, -1, 1]
    y = dy[(j + 1) % 6] + dy[j] * (i - 1) + dy[(j + 2) % 6] * k
    x = dx[(j + 1) % 6] + dx[j] * (i - 1) + dx[(j + 2) % 6] * k
    print(x, y)