def inc(arr):
    for i in range(len(arr) - 1, -1, -1):
        if arr[i] == 0:
            for j in range(len(arr) - 1, i, -1):
                arr[j] = 0
            arr[i] = 1
            return arr


def proveralo1(a, arr):
    return [a[i] for i in range(len(arr)) if arr[i] == 1]


def proveralo2(c):
    f = 0
    for value in c:
        if f == 1 and value == 0:
            return False
        if f == 0 and value == 1:
            f = 1
    return True


n = int(input())
arr = [0] * n
a = list(map(int, input().split()))
s = 0
c1 = []
while True:
    arr = inc(arr)
    c = proveralo1(a, arr)
    r = len(c) if proveralo2(c) else 0
    if r > s:
        s = r
        c1 = c
    if inc(arr) is None:
        break
print(s)
