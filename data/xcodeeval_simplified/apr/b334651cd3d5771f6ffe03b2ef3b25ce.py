l, r = map(int, input().split())


def cnt(x):
    ret = 0
    for i in range(1, x + 1):
        s = str(i)
        if s[0] == s[-1]:
            ret += 1
    return ret


def cnt2(x):
    s = str(x)
    L = len(s)
    if L >= 2 and x == 10 ** (L - 1):
        return cnt2(10 ** (L - 1) - 1)
    if L <= 1:
        return x
    elif L <= 2:
        while x // 10 != x % 10:
            x -= 1
        return 9 + x // 10
    else:
        ret = int("1" + "0" * (L - 3) + "8")
        num = list(str(x))
        if num[0] != num[-1]:
            if int(num[0]) > int(num[-1]):
                how = int(num[-1]) + 10 - int(num[0])
            else:
                how = int(num[-1]) - int(num[0])
            x -= how
        num = str(x)
        d = x % 10
        ret += (d - 1) * int("9" * (L - 2)) + int(num[1:-1]) + d
        return ret


print(cnt2(r) - cnt(l - 1))
