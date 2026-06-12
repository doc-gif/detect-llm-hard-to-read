n = eval(input())

area = 0
p1 = []
p2 = []
ps = []
xl, xu, yl, yu = 0, 1 << 28, 0, 1 << 28
for i in range(n):
    in_ = input().split()
    p1.append(tuple(map(int, in_[0:2])))
    p2.append(tuple(map(int, in_[2:4])))
    xl = min(xl, ps[-2][0], ps[-1][0])
    xu = max(xu, ps[-2][0], ps[-1][0])
    yl = min(yl, ps[-2][1], ps[-1][1])
    yu = max(yu, ps[-2][1], ps[-1][1])

ok = True
for p in p2:
    q = p
    if p[0] < xu:
        q = (q[0] + 0.5, q[1])
    if p[1] < yu:
        q = (q[0], q[1] + 0.5)
    for i in range(n):
        if not (p1[i][0] <= p[0] <= p2[i][0] and p1[i][1] <= p[1] <= p2[i][1]):
            ok = False
for p in p1:
    q = p
    if xl < p[0]:
        q = (q[0] - 0.5, q[1])
    if yl < p[1]:
        q = (q[0], q[1] - 0.5)
    for i in range(n):
        if not (p1[i][0] <= p[0] <= p2[i][0] and p1[i][1] <= p[1] <= p2[i][1]):
            ok = False

print('YES' if ok else 'NO')
