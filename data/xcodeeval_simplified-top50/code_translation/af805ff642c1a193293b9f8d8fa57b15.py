def main():
    n, m, k, x, y = map(int, input().split())
    if n == 1:
        base = k // m
        remainder = k % m
        if remainder == 0:
            print(base, base, base)
        else:
            sergei = base + (1 if y <= remainder else 0)
            print(base + 1, base, sergei)
        return
    max_ans = -(10**20)
    min_ans = 10**20
    sergei_ans = 0
    for i in range(1, n + 1):
        inc1 = 2 * (n - i) * m
        inc2 = 2 * (i - 1) * m
        for j in range(1, m + 1):
            lo, hi = -1, 10**18
            while hi - lo > 1:
                mid = (lo + hi) // 2
                times2 = mid // 2 if inc2 != 0 else 0
                times1 = mid - times2
                if inc1 == 0:
                    times1, times2 = 0, mid
                total = (i - 1) * m + j + inc1 * times1 + inc2 * times2
                if total <= k:
                    lo = mid
                else:
                    hi = mid - 1
            times2 = hi // 2 if inc2 != 0 else 0
            times1 = hi - times2
            if inc1 == 0:
                times1, times2 = 0, hi
            total = (i - 1) * m + j + inc1 * times1 + inc2 * times2
            ans = hi + 1 if total <= k else hi
            if i == x and j == y:
                sergei_ans = ans
            if ans > max_ans:
                max_ans = ans
            if ans < min_ans:
                min_ans = ans
    print(max_ans, min_ans, sergei_ans)
main()