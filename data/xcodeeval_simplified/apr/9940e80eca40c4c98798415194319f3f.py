def get_divisors(num):
    divisors = []
    for i in range(1, num + 1):
        if num % i == 0:
            divisors.append(i)
    return divisors


def get_common_divisors(a, b):
    common = []
    for i in range(max(a, b)):
        if i in get_divisors(a) and i in get_divisors(b) and i not in common:
            common.append(i)
    return common


wh, lh, lw = map(int, input().split())
ph = get_common_divisors(wh, lh)
pw = get_common_divisors(wh, lw)
pl = get_common_divisors(lh, lw)
l, w, h = 1, 1, 1
while True:
    if wh == w * h and lh == l * h and lw == l * w:
        break
    for i in ph:
        for j in pw:
            for k in pl:
                if wh == i * j and lh == k * i and lw == k * j:
                    h, w, l = i, j, k
                    break
            if wh == w * h and lh == l * h and lw == l * w:
                break
        if wh == w * h and lh == l * h and lw == l * w:
            break
print((l + h + w) * 4)
