import math
n, k = map(int, input().split())
arr = list(map(int, input().split()))
i = 1
j = (sum(arr) + k * i) / (len(arr) + i)
if j - math.trunc(j) >= 0.5:
    j = math.ceil(j)
else:
    j = math.trunc(j)
if j == k:
    print(0)
else:
    while True:
        j = (sum(arr) + k * i) / (len(arr) + i)
        if j - math.trunc(j) >= 0.5:
            j = math.ceil(j)
        else:
            j = math.trunc(j)
        if j == k:
            print(i)
            break
        i += 1