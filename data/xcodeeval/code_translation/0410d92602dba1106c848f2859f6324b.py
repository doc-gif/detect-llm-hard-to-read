#!/usr/bin/python

# http://codeforces.com/problemset/problem/673/A


# define function
def watching_minute(n, a):
    if a[0] > 15:
        return 15
    elif len(a) == 1:
        return a[0] + 15
    else:
        for i in range(len(a) - 1):
            if a[i+1] - a[i] > 15:
                return a[i] + 15

            if a[i+1] >= 75 or a[i] >= 75:
                return 90

            # check last number
            if i + 1 == len(a) - 1 and a[i+1] < 75:
                return a[i + 1] + 15

# call function
n = int(input())
a = [int(i) for i in input().split()]
print(watching_minute(n, a))
