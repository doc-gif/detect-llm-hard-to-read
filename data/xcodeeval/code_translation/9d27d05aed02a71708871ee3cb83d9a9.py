from sys import stdin


n = int(stdin.readline())


def eq(m1, m2):
    for i in range(n):
        if m1[i] != m2[i]:
            return False
    return True


def fleq(m1, m2):
    return eq(m1, m2) or eq(m1, fliph(m2)) or eq(m1, flipv(m2))


def fliph(m):
    return [row[::-1] for row in m]


def flipv(m):
    return m[::-1]


def rot(m):
    mr = ['' for _ in range(n)]
    for i in range(n):
        x = ''
        for j in range(n):
            x = x + m[j][n-i-1]
        mr[i] = x
    return mr


u = [stdin.readline()[:-1] for _ in range(n)]
v = [stdin.readline()[:-1] for _ in range(n)]
v90 = rot(v)
v180 = rot(v90)
v270 = rot(v180)

if fleq(u, v) or fleq(u, v90) or fleq(u, v180) or fleq(u, v270):
    print('Yes')
else:
    print('No')
