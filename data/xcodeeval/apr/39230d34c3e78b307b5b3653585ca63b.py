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
for i in range(8):
    if c[x1][i] != 1:
        c[x1][i] = 1
    else:
        break
for i in range(8):
    if c[x2][i] != 1:
        c[x2][i] = 1
    else:
        break
for i in range(8):
    if c[i][y1] != 1:
        c[i][y1] = 1
    else:
        break 
for i in range(8):
    if c[i][y2] != 1:
        c[i][y2] = 1
    else:
        break
c[x1][y1] = 0
c[x2][y2] = 0 
for i in range(-1,2):
    for j in range(-1,2):
        if x3 + i> -1 and x3+ i < 8 and y3+j > -1 and y3+j < 8:
            c[x3 + i][y3 + j] = 1

for i in range(-1,2):
    for j in range(-1,2):
        if x4 + i> -1 and x4+ i < 8 and y4+j > -1 and y4+j <8 :
            if c[x4 + i][y4 + j] == 0:
                print("OTHER")
                sys.exit()
print("CHECKMATE")
            
