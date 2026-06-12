import itertools
import sys


def rl():
    return sys.stdin.readline().strip()


def rn():
    return list(map(int, sys.stdin.readline().strip().split()))


def rln(n):
    l = [None] * n
    for i in range(n):
        l[i] = int(rl())
    return l


def solve(t):
    for e in t:
        if e[0] + e[1] == e[2] + e[3] or e[0] == e[1] + e[2] + e[3]:
            return True
    return False


if __name__ == '__main__':
    tab = rn()
    t = itertools.permutations(tab)
    print('YES' if solve(t) else 'NO')
