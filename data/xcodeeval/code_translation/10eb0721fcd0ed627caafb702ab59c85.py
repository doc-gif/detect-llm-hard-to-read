t = [int(x) for x in input().split()] + [int(x) for x in input().split()] 
p = []
for i in range(8):
    p.append((t[2*i],t[2*i+1]))
def x(): 
    xmin = min([p[0][0],p[1][0],p[2][0],p[3][0]])
    xmax = max([p[0][0],p[1][0],p[2][0],p[3][0]])
    ymin = min([p[0][1],p[1][1],p[2][1],p[3][1]])
    ymax = max([p[0][1],p[1][1],p[2][1],p[3][1]])
    xc, yc = ((p[4][0] + p[6][0]) / 2.0,(p[4][1] + p[6][1]) / 2.0)
    if xc >= xmin and xc <= xmax and yc >= ymin and yc <= ymax:
        print("YES")
        return
    for i in range(4, 8):
        x, y = p[i]  
        if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
            print("YES")
            return
    b = [p[4][1] - p[4][0], p[6][1] - p[6][0],p[4][1] + p[4][0], p[6][1] + p[6][0]]
    for i in range(4):
        x, y = p[i]
        s = [y - x, y + x]
        if s[0] >= min([b[0], b[1]]) and s[0] <= max([b[0], b[1]]) and s[1] >= min([b[2], b[3]]) and s[1] <= max([b[2], b[3]]):
            print("YES")
            return
    print("NO")
x()



