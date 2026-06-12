import sys
n = int(sys.stdin.readline())
a = int(sys.stdin.readline())
g = []
t = a
for _ in range(n):
    if t % 10 != 0:
        g.append(t % 10)
    t //= 10
def primes(n):
    primfac = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            primfac.append(d)
            n //= d
        d += 1
    if n > 1:
        primfac.append(n)
    return primfac
b = []
for i in g:
    if i != 1:
        gg = 2
        for j in range(2, i + 1):
            if gg < max(primes(j)):
                gg = max(primes(j))
        b.append(gg)
        if i == 9:
            b.extend([2, 3, 3])
        else:
            for k in range(gg + 1, i + 1):
                if k == 6:
                    b.append(3)
                else:
                    b.extend(primes(k))
print(int("".join(map(str, reversed(sorted(b))))))