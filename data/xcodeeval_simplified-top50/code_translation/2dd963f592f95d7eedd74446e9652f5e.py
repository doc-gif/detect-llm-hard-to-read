def binary_search(n, k, low, high):
    while low <= high:
        mid = (high + low) // 2
        total = ((k * (k + 1)) // 2 - 1) - (((mid - 1) * mid) // 2 - 1) - (k - 2)
        if total == n:
            return k - mid + 1
        if total > n:
            low = mid + 1
        elif total < n:
            high = mid - 1
    if total > n:
        mid += 1
    return k - mid + 1
def solve():
    n, k = map(int, input().split())
    if n == 1:
        return 0
    if (k * (k + 1) // 2) - (k - 2) <= n:
        return -1
    if k >= n:
        return 1
    return binary_search(n, k, 2, k)
print(solve())