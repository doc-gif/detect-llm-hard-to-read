n, l = map(int, input().split())
d1 = list(map(int, input().split()))
d2 = list(map(int, input().split()))
flag = False
for i in range(l):
    for j in range(n):
        d1[j] -= 1
        if d1[j] == -1:
            d1[j] = l - 1
    d1.sort()
    if d1 == d2:
        flag = True
print("YES" if flag else "NO")