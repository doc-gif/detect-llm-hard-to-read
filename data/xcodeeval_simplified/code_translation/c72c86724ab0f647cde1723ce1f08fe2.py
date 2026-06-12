n = int(input())
cnt = True
a = []
Mark = []
for _ in range(n):
    a.append(input().split())
if n == 1:
    for i in range(6):
        Mark.append(a[0][i])
elif n == 3:
    for i in range(6):
        for j in range(6):
            for p in range(6):
                Mark.append(a[0][i])
                Mark.append(a[1][j])
                Mark.append(a[2][p])
                Mark.append(a[0][i] + a[1][j])
                Mark.append(a[0][i] + a[2][p])
                Mark.append(a[1][j] + a[2][p])
                Mark.append(a[1][j] + a[0][i])
                Mark.append(a[2][p] + a[0][i])
                Mark.append(a[2][p] + a[1][j])
                Mark.append(a[0][i] + a[1][j] + a[2][p])
                Mark.append(a[0][i] + a[2][p] + a[1][j])
                Mark.append(a[1][j] + a[2][p] + a[0][i])
                Mark.append(a[1][j] + a[0][i] + a[2][p])
                Mark.append(a[2][p] + a[0][i] + a[1][j])
                Mark.append(a[2][p] + a[1][j] + a[0][i])
else:
    for i in range(6):
        for j in range(6):
            Mark.append(a[0][i])
            Mark.append(a[1][j])
            Mark.append(a[0][i] + a[1][j])
            Mark.append(a[1][j] + a[0][i])
Mark = [int(x) for x in Mark]
Mark.sort()
for i in range(1, Mark[-1]):
    if Mark.count(i) > 0:
        pass
    else:
        print(i - 1)
        cnt = False
        break
if cnt:
    print(Mark[-1])