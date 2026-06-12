def inc(arr):
    for i in range(len(arr) - 1, -1, -1):
        w = arr[i]
        if w == 0:
            for j in range(len(arr) - 1, i, -1):
                arr[j] = 0
            arr[i] = 1
            return arr


def proveralo1(a, arr):
    c = []
    for i in range(len(arr)):
        if arr[i] == 1:
            c.append(a[i])
    return c
def proveralo2(c):
    f = 0
    for i in range(len(c)):
        if f == 1 and c[i] == 0:
            return False
        if f == 0 and c[i] == 1:
            f = 1
    return True


n = int(input())
arr = [0] * n
a = list(map(int,input().split()))
s = 0
c1 = []
while True:
    c = []
    r = 0
    arr = inc(arr)
    c = proveralo1(a,arr)
    if proveralo2(c) == True:
        r = len(c)
    if r > s:
        s = r
        c1 = c
    if inc(arr) == None:
        break
print(s)