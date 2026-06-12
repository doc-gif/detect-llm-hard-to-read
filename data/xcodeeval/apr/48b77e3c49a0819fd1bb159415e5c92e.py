# https://codeforces.com/problemset/problem/575/H

import sys
import math

mod = pow(10, 9) + 7


def main():
    # sys.stdin = open('E:\\Sublime\\in.txt', 'r')
    # sys.stdout = open('E:\\Sublime\\out.txt', 'w')
    # sys.stderr = open('E:\\Sublime\\err.txt', 'w')

    n = int(sys.stdin.readline().strip())
    # a, b = map(int, sys.stdin.readline().strip().split()[:2])

    # C(n+1, 2n + 2) = (2n+2)! : (n+1)! : n+1!
    # = (n+2)(n+3)...(2n+2) /

    t = 1
    m = 1
    for i in range(1, n + 2):
        t *= (n + i + 1) % mod
        m *= i % mod
    print((t // m - 1) % mod)


if __name__ == '__main__':
    main()

# hajj
#  　　　　　　 ＿＿
# 　　　　　／＞　　フ
# 　　　　　| 　_　 _ l
# 　 　　　／` ミ＿xノ
# 　　 　 /　　　 　 |
# 　　　 /　 ヽ　　 ﾉ
# 　 　 │　　|　|　|
# 　／￣|　　 |　|　|
# 　| (￣ヽ＿_ヽ_)__)
# 　＼二つ
