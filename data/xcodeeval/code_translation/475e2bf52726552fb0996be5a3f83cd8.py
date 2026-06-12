def vec(a, b):
    return a[0] * b[1] - a[1] * b[0]


a_x, a_y = [int(i) for i in input().split()]
b_x, b_y = [int(i) for i in input().split()]
c_x, c_y = [int(i) for i in input().split()]
a, b, c = [a_x, a_y], [b_x, b_y], [c_x, c_y]
s, d = [b[0] - a[0], b[1] - a[1]], [c[0] - a[0], c[1] - a[1]]
e = vec(s, d)
if e < 0:
    print('RIGHT')
elif e > 0:
    print('LEFT')
else:
    print("TOWARDS")
