import math
def UnusualSeq(a, b):
    if b % a != 0:
        print(0)
    else:
        b //= a
        divisors = set()
        sqrt_b = int(math.sqrt(b))
        for i in range(1, sqrt_b + 1):
            if b % i == 0:
                divisors.add(i)
                divisors.add(b // i)
        divisors = sorted(divisors)
        f = divisors[:]
        mod = 10**9 + 7
        for i in range(len(f)):
            f[i] = pow(2, divisors[i] - 1, mod)
            for j in range(i):
                if divisors[i] % divisors[j] == 0:
                    f[i] -= f[j]
        print(f[-1] % mod)
a, b = map(int, input().split())
UnusualSeq(a, b)