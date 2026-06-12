(x11, y11, x12, y12, x13, y13, x14, y14) = map(int, input().split())

(x21, y21, x22, y22, x23, y23, x24, y24) = map(int, input().split())

def xxx(x1, y1, x2, y2, x3, y3):
    return (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)

flag = False

if xxx(x11, y11, x12, y12, x21, y21) >= 0 and xxx(x12, y12, x13, y13, x21, y21) >= 0 and xxx(x13, y13, x14, y14, x21, y21) >= 0 and xxx(x14, y14, x11, y11, x21, y21) >= 0:
    flag = True


if xxx(x11, y11, x12, y12, x22, y22) >= 0 and xxx(x12, y12, x13, y13, x22, y22) >= 0 and xxx(x13, y13, x14, y14, x22, y22) >= 0 and xxx(x14, y14, x11, y11, x22, y22) >= 0:
    flag = True
    
if xxx(x11, y11, x12, y12, x23, y23) >= 0 and xxx(x12, y12, x13, y13, x23, y23) >= 0 and xxx(x13, y13, x14, y14, x23, y23) >= 0 and xxx(x14, y14, x11, y11, x23, y23) >= 0:
    flag = True

if xxx(x11, y11, x12, y12, x24, y24) >= 0 and xxx(x12, y12, x13, y13, x24, y24) >= 0 and xxx(x13, y13, x14, y14, x24, y24) >= 0 and xxx(x14, y14, x11, y11, x24, y24) >= 0:
    flag = True

x = x21 + (x23 - x21) / 2
y = y21 + (y23 - y21) / 2

if xxx(x11, y11, x12, y12, x, y) >= 0 and xxx(x12, y12, x13, y13, x, y) >= 0 and xxx(x13, y13, x14, y14, x, y) >= 0 and xxx(x14, y14, x11, y11, x, y) >= 0:
    flag = True



    

if xxx(x21, y21, x22, y22, x11, y11) >= 0 and xxx(x22, y22, x23, y23, x11, y11) >= 0 and xxx(x23, y23, x24, y24, x11, y11) >= 0 and xxx(x24, y24, x21, y21, x11, y11) >= 0:
    flag = True


if xxx(x21, y21, x22, y22, x12, y12) >= 0 and xxx(x22, y22, x23, y23, x12, y12) >= 0 and xxx(x23, y23, x24, y24, x12, y12) >= 0 and xxx(x24, y24, x21, y21, x12, y2) >= 0:
    flag = True
    
if xxx(x21, y21, x22, y22, x13, y13) >= 0 and xxx(x22, y22, x23, y23, x13, y13) >= 0 and xxx(x23, y23, x24, y24, x13, y13) >= 0 and xxx(x24, y24, x21, y21, x13, y13) >= 0:
    flag = True

if xxx(x21, y21, x22, y22, x14, y14) >= 0 and xxx(x22, y22, x23, y23, x14, y14) >= 0 and xxx(x23, y23, x24, y24, x14, y14) >= 0 and xxx(x24, y24, x21, y21, x14, y14) >= 0:
    flag = True

x = x11 + (x13 - x11) / 2
y = y11 + (y13 - y11) / 2

if xxx(x21, y21, x22, y22, x, y) >= 0 and xxx(x22, y22, x23, y23, x, y) >= 0 and xxx(x23, y23, x24, y24, x, y) >= 0 and xxx(x24, y24, x21, y21, x, y) >= 0:
    flag = True






if xxx(x11, y11, x12, y12, x21, y21) <= 0 and xxx(x12, y12, x13, y13, x21, y21) <= 0 and xxx(x13, y13, x14, y14, x21, y21) <= 0 and xxx(x14, y14, x11, y11, x21, y21) <= 0:
    flag = True


if xxx(x11, y11, x12, y12, x22, y22) <= 0 and xxx(x12, y12, x13, y13, x22, y22) <= 0 and xxx(x13, y13, x14, y14, x22, y22) <= 0 and xxx(x14, y14, x11, y11, x22, y22) <= 0:
    flag = True
    
if xxx(x11, y11, x12, y12, x23, y23) <= 0 and xxx(x12, y12, x13, y13, x23, y23) <= 0 and xxx(x13, y13, x14, y14, x23, y23) <= 0 and xxx(x14, y14, x11, y11, x23, y23) <= 0:
    flag = True

if xxx(x11, y11, x12, y12, x24, y24) <= 0 and xxx(x12, y12, x13, y13, x24, y24) <= 0 and xxx(x13, y13, x14, y14, x24, y24) <= 0 and xxx(x14, y14, x11, y11, x24, y24) <= 0:
    flag = True

x = x21 + (x23 - x21) / 2
y = y21 + (y23 - y21) / 2

if xxx(x11, y11, x12, y12, x, y) <= 0 and xxx(x12, y12, x13, y13, x, y) <= 0 and xxx(x13, y13, x14, y14, x, y) <= 0 and xxx(x14, y14, x11, y11, x, y) <= 0:
    flag = True



    

if xxx(x21, y21, x22, y22, x11, y11) <= 0 and xxx(x22, y22, x23, y23, x11, y11) <= 0 and xxx(x23, y23, x24, y24, x11, y11) <= 0 and xxx(x24, y24, x21, y21, x11, y11) <= 0:
    flag = True


if xxx(x21, y21, x22, y22, x12, y12) <= 0 and xxx(x22, y22, x23, y23, x12, y12) <= 0 and xxx(x23, y23, x24, y24, x12, y12) <= 0 and xxx(x24, y24, x21, y21, x12, y12) <= 0:
    flag = True
    
if xxx(x21, y21, x22, y22, x13, y13) <= 0 and xxx(x22, y22, x23, y23, x13, y13) <= 0 and xxx(x23, y23, x24, y24, x13, y13) <= 0 and xxx(x24, y24, x21, y21, x13, y13) <= 0:
    flag = True

if xxx(x21, y21, x22, y22, x14, y14) <= 0 and xxx(x22, y22, x23, y23, x14, y14) <= 0 and xxx(x23, y23, x24, y24, x14, y14) <= 0 and xxx(x24, y24, x21, y21, x14, y14) <= 0:
    flag = True

x = x11 + (x13 - x11) / 2
y = y11 + (y13 - y11) / 2

if xxx(x21, y21, x22, y22, x, y) <= 0 and xxx(x22, y22, x23, y23, x, y) <= 0 and xxx(x23, y23, x24, y24, x, y) <= 0 and xxx(x24, y24, x21, y21, x, y) <= 0:
    flag = True


    
if flag:
    print("YES")
else:
    print("NO")
