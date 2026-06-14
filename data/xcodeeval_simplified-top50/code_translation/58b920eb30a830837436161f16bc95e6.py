import sys
input = sys.stdin.readline
read_ints = lambda: map(int, input().split())
n, m, k = read_ints()
l = list(read_ints())
l.sort(reverse=True)
count = 0
if k >= m:
    count = 0
else:
    for i in range(n):
        count += 1
        k += l[i] - 1
        if k >= m:
            break
        if (k == 0 or l[i] == 1) or k == 0:
            count = -1
            break
    if k < m:
        count = -1
print(count)