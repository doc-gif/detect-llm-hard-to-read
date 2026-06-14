def isAtLeastHalf(k, n):
    V = 0
    P = 0
    least = (n // 2) + 1 if n % 2 else n // 2
    res = False
    while n > 0 and k > 0:
        if n >= k:
            V += k
            n -= k
        else:
            V += n
            n = 0
        temp = n // 10
        P += temp
        n -= temp
        if V >= least:
            res = True
            break
    return res
def searchMiniumCandies(n, l, r, res=-1):
    if r >= l:
        mid = l + (r - l) // 2
        if isAtLeastHalf(mid, n):
            res = mid
            return searchMiniumCandies(n, l, mid - 1, res)
        else:
            return searchMiniumCandies(n, mid + 1, r, res)
    else:
        return res
n = int(input())
print(searchMiniumCandies(n, 0, n))