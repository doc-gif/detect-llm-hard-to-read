from bisect import insort

n, m = [int(x) for x in input().split()]

students = [int(x) for x in input().split()]

s = 0

heap = []

std = []

for i in students:

    if s + i > m:
        std = heap.copy()
        t = 0
        q = s
        while q + i > m:
            q -= std.pop()
            t += 1
        print(t, end=' ')
    else:
        print("0 ", end = '')
    s += i
    insort(heap, i)
