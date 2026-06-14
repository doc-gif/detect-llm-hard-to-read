n = int(input())
l = list(input())
a = l[:n]
b = l[n : 2 * n]
a.sort()
b.sort()
strictly_less = True
strictly_greater = True
early_exit = False
for i in range(n):
    if a[i] > b[i]:
        strictly_less = False
    else:
        strictly_greater = False
    if (not strictly_less and not strictly_greater) or a[i] == b[i]:
        print("NO")
        early_exit = True
        break
if not early_exit:
    print("YES")