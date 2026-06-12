h, m, s, t1, t2 = map(int, input().split())
m += s / 60
h += m / 60
m /= 5
s /= 5
h %= 12
m %= 12
s %= 12
T1 = min(t1, t2)
T2 = max(t1, t2)
all_inside = T1 < h < T2 and T1 < m < T2 and T1 < s < T2
all_outside = not (T1 < h < T2 or T1 < m < T2 or T1 < s < T2)
if all_inside or all_outside:
    print("YES")
else:
    print("NO")