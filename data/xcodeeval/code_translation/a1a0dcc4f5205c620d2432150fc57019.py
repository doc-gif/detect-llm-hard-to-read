a, b = input().split()
a = int(a)
b = int(b)
c = b
d = ''
t = ''

n = [a]
while a != c:
    if (c % 2 == 0) and (a <= c):
        c = c / 2
        d = d + '1'
    elif (c - 1) % 10 == 0 and (a <= c):
        c = (c - 1) / 10
        d = d + '2'
    else:
        break
if a == c:
    print('YES')
    t = d[::-1]
    f = len(t)
    print(len(t) + 1)
    for i in range (1, f + 1):
        if t[i-1:i] == '1':
            a = a * 2
            n.append(a)
        else:
            a = (a * 10) + 1
            n.append(a)
    for i in range(0, f + 1):
        print(n[i], end = ' ')
elif c != a:
    print('NO')


