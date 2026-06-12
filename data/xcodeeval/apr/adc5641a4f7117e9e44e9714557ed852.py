from sys import stdin, stdout
import sys
sys.setrecursionlimit(1500)


# 7 3
# n % 2 % 3 % 4 = n % 3 % 2 % 4
# 8 % 3 % 6 = 2 = 8 % 6 % 3 =
# 8 % 5 % 10 = 3 = 8 % 10 % 5 = 3
# 8 % 2 % 5, 8 % 5 % 2

# 1 => (2 3) 4 5 6 =>
# 1 => (2, 3) 4 => 3*2 / 2
# 1 => any
# 2 => 2*1, 2*2, 2*3, 2*4
# 3 => 3*1, 3*2, 3*3, 3*4
# 5 => 5*1, 5*2, 5*3, 5*4
def modular_stability(n, k):

    if k > n:
        return 0

    if k == 1:
        return n

    res = 0
    # 1
    res += com(n-1, k-1)
    res %= 998244353

    # prime numbers
    for i in range(2, n+1):
        #if isprime(i):
        cnt = n // i
        if cnt == k:
            res += 1
        elif cnt > k:
            res += com(cnt-1, k-1)
            res %= 998244353

    #print(faca)
    return res


def isprime(n):

    j = 2
    while j*j <= n:
        if n%j == 0:
            return False
        j += 1

    return True


def com(p1, p2):
    return fac(p1) // fac(p1-p2) // fac(p2)


faca = [0, 1]
def fac(n):
    if len(faca) > n:
        return faca[n]
    r = n*fac(n-1)
    faca.append(r)

    return r


if __name__ == '__main__':
    (n,k) = list(map(int, stdin.readline().split()))
    for i in range(1, n+1):
        fac(i)

    print(modular_stability(n, k))
