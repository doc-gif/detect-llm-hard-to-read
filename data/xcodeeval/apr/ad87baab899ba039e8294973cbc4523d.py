def inp(dtype=str, strip=True):
    s = input()
    res = [dtype(p) for p in s.split()]
    res = res[0] if len(res) == 1 and strip else res
    return res


def problem1():
    n, m = inp(int)
    s = inp(strip=False)
    t = inp(strip=False)
    q = inp(int)
    for _ in range(q):
        y = inp(int) - 1
        print(s[y % n] + t[y % m])


def problem2():
    n = inp(int)
    res = 0
    noascent_mins = [0 for _ in range(n)]
    noascent_maxs = [0 for _ in range(n)]
    noascent_cnt = 0
    for i in range(n):
        s = inp(int, strip=False)
        assert s[0] == len(s) - 1
        s = s[1:]
        ssort = sorted(s, reverse=True)
        mn, mx = ssort[-1], ssort[0]
        has_ascent = (s != ssort) and (mn < mx)
        if has_ascent:
            num = 2 * (n - i + noascent_cnt) - 1
            res += num
        else:
            # num1 = sum([mn_prev < mx for mn_prev in noascent_mins])
            # num2 = sum([mx_prev > mn for mx_prev in noascent_maxs])
            noascent_mins[noascent_cnt] = mn
            noascent_maxs[noascent_cnt] = mx
            noascent_cnt += 1
            # res += num1 + num2

    noascent_maxs = noascent_maxs[:noascent_cnt]
    noascent_mins = noascent_mins[:noascent_cnt]

    noascent_mins = sorted(noascent_mins)
    noascent_maxs = sorted(noascent_maxs)

    n = noascent_cnt
    i = 0
    for j in range(n):
        while (i < n) and (noascent_mins[i] < noascent_maxs[j]):
            i += 1

        res += i

    print(res)


def problem3():
    n, m = inp(int)
    res = 0
    factorials = [1 for i in range(n + 1)]
    for k in range(1, n + 1):
        factorials[k] = factorials[k - 1] * k
    for k in range(1, n + 1):
        res += (((n - k + 1) ** 2) * factorials[k] * factorials[n-k]) % m

    print(res % m)


def problem4():
    pass


def problem5():
    pass


if __name__ == '__main__':
    # problem1()
    # problem2()
    problem3()
    # problem4()
    # problem5()
