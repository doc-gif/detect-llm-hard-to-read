
n = int(input())
x = input()
for i in range(0, 9*n+1):
    total = 0
    ok = 0
    for c in x:
        total = total + int(c)
        if total == i:
            total = 0
            ok = ok+1
        elif total > i:
            ok = 0
    if ok > 1 and total == 0:
        print("YES")
        exit(0)
print("NO")