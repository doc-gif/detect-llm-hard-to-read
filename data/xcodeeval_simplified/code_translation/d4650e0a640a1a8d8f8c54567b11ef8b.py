import sys
def sum_(a):
    return max(0, a * (a + 1) // 2)
def check(a):
    if a * n <= m:
        return True
    a -= 1
    ans = n
    t1 = a - k + 1
    if t1 >= 0:
        ans += sum_(a) - sum_(t1 - 1)
    else:
        ans += sum_(a)
    z = n - k + 1
    t2 = a - z + 1
    if t2 >= 0:
        ans += sum_(a - 1) - sum_(t2 - 1)
    else:
        ans += sum_(a - 1)
    return ans <= m
def bins():
    left = 1
    right = m + 1
    while left + 1 != right:
        mid = (left + right) // 2
        if check(mid):
            left = mid
        else:
            right = mid
    print(left)
n, m, k = map(int, input().split())
bins()