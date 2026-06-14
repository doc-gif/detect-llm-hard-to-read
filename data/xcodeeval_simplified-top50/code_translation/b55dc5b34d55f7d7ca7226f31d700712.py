def main():
    from math import sqrt
    m, n, k = map(int, input().split())
    if n < m:
        n, m = m, n
    low, high = 1, k + 1
    while low + 1 < high:
        mid = (low + high) // 2
        t = mid - 1
        v = min(int(sqrt(t)), m)
        tn, tm = (t - 1) // m, t // n
        vv = [t // i for i in range(tm + 1, v + 1)]
        term1 = t // n * (n + m)
        term2 = sum(vv) * 2
        term3 = max(min((tn - tm), len(vv)) * m, 0)
        term4 = v * v
        term5 = sum(vv[: max(min(tn - tm, len(vv)), 0)])
        if term1 + term2 + term3 - term4 - term5 < k:
            low = mid
        else:
            high = mid
    print(low)
if __name__ == "__main__":
    main()