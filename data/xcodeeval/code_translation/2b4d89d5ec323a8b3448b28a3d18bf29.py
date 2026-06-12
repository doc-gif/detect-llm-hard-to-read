import sys

def solve():
    a, b = map(int, input().split())
    c, d = map(int, input().split())

    if b < d:
        a, c = c, a
        b, d = d, b

    for i in range(c):
        if (b - d + i*a) % c == 0:
            ans = b + i*a
            print(ans)
            return

    print(-1)

if __name__ == '__main__':
    solve()