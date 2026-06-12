import sys
b = 'sabcdefgh'
a1,a2,a3,a4 = map(str,input().split())
x1 = b.index(a1[0])-1
y1 = int(a1[1]) -1
x2 = b.index(a2[0])-1
y2 = int(a2[1]) -1
x3 = b.index(a3[0])-1
y3 = int(a3[1]) -1
x4 = b.index(a4[0])-1
y4 = int(a4[1]) -1
c = []
for i in range(8):
    c.append([0]*8)
pr = 0
pr1 = 0
pr4 = 0
pr3 = 0
for i in range(1,8):
    if y1 - i > -1 and pr == 0:
        if (y1 - i == y2 and x1 == x2) or (y1 - i == y3 and x1 == x3):
            c[x1][y1 - i] = 1
            pr = 1
        else:
            c[x1][y1 - i] = 1
    if y1 + i < 8 and pr1 == 0:
        if (y1 + i == y2 and x1 == x2) or (y1 + i == y3 and x1 == x3):
            c[x1][y1 + i] = 1
            pr1 = 1
        else:
            c[x1][y1 + i] = 1
    if y2 - i > -1 and pr3 == 0:
        if (y2 - i == y1 and x1 == x2) or (y2 - i == y3 and x2== x3):
            c[x2][y2 - i] = 1
            pr3 = 1
        else:
            c[x2][y2 - i] = 1
    if y2 + i < 8 and pr4 == 0:
        if (y3 + i == y1 and x1 == x2) or (y2 + i == y3 and x2 == x3):
            c[x2][y2 + i] = 1
            pr4 = 1
        else:
            c[x2][y2 + i] = 1
pr = 0
pr1 = 0
pr2 = 0
pr3 = 0
for i in range(1,8):
    if x1 - i > -1 and pr == 0:
        if (x1 - i == x2 and y1 == y2) or (x1 - i == x3 and y1 == y3):
            c[x1 - i][y1] = 1
            pr = 1
        else:
            c[x1 - i][y1] = 1
    if x2 - i > -1 and pr1 == 0:
        if (x2 - i == x1 and y1 == y2) or (x2 - i == x3 and y2 == y3):
            c[x2 - i][y2] = 1
            pr1 = 1
        else:
            c[x2 - i][y2] = 1
    if x1 + i < 8 and pr2 == 0:
        if (x1 + i == x2 and y1 == y2) or (x1 + i == x3 and y1 == y3):
            c[x1 + i][y1] = 1
            pr2 = 1
        else:
            c[x1 + i][y1] = 1
    if x2 + i < 8 and pr3 == 0:
        if (x2 + i == x1 and y1 == y2) or (x2 + i == x3 and y2 == y3):
            c[x2 + i][y2] = 1
            pr3= 1
        else:
            c[x2 + i][y2] = 1
for i in range(-1,2):
    for j in range(-1,2):
        if x3 + i < 8 and x3 + i > -1 and y3 + j < 8 and y3 + j > -1:
            c[x3 + i][y3+j] = 1

for i in range(-1,2):
    for j in range(-1,2):
        if x4 + i < 8 and x4 + i > -1 and y4 + j < 8 and y4 + j > -1:
            if c[x4 + i][y4+j] == 0:
                print("OTHER")
                sys.exit()
print("CHECKMATE")
