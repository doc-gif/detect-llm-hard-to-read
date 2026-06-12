from collections import Counter

def primes(n):
    primfac = []
    cnt = Counter()
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            cnt[d] += 1
            # primfac.append(d)
            n //= d
        d += 1
    if n > 1:
        cnt[n] += 1
        # primfac.append(n)


    return list(cnt.values())


def run():
    b = int(input())
    occ = primes(b)
    res = 1
    for e in occ:
        res *= e + 1

    print(res)


if __name__ == '__main__':
    run()
