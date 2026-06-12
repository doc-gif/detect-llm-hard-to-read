a = list(map(int,input().split()))
maxi = -1
for i in range(14):
    s = 0
    if a[i] != 0:
        cel = a[i] // 14
        ost = a[i] % 14

        for ty in range(1,14):
            if i + ty > 13:
                i -= 14
            su = a[i + ty] + cel
            if ty <= ost:
                su += 1
            if su % 2 == 0:
                s += su
        if cel % 2 == 0:
            s += cel
    if s > maxi:
        maxi = s
print(maxi)
