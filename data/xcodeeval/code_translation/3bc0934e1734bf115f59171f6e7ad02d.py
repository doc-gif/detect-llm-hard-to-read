s = []
for i in range(2):
    a1 = input()
    a2 = input()
    a = a1 + a2
    k = a.index('X')
    if k == 0:
        x = a[2]+a[1]+a[3]
    elif k == 1:
        x = a[2]+a[0]+a[3]
    elif k == 2:
        x = a[3]+a[0]+a[1]
    else:
        x = a[2]+a[0]+a[1]
    s.append(x)
#print(s)
b1 = s[0][1] + s[0][2] + s[0][0]
b2 = s[0][2] + s[0][0] + s[0][1]
if s[0] == s[1] or s[1] == b1 or s[1] == b2:
    print('YES')
else:
    print('NO')