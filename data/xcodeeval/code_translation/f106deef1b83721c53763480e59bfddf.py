l = []

for _ in range(11):
    s = input().replace(' ', '')
    if len(s):
        l.append(list(s))

x, y = map(int, input().split())

x -= 1
y -= 1

x %= 3
y %= 3

ok = False

for i in range(x * 3, x * 3 + 3):
    for j in range(y * 3, y * 3 + 3):
        if l[i][j] == '.':
            ok = True
            l[i][j] = '!'

if not ok:
    for i in range(9):
        for j in range(9):
            if l[i][j] == '.':
                l[i][j] = '!'

for i in range(9):
    for j in range(9):
        print(l[i][j], end='')
        if j % 3 == 2:
            print(' ', end='')
    print()
    if i % 3 == 2:
            print()
