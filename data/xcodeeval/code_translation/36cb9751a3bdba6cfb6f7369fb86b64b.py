curX, curY = (int(x) for x in input().split())

x = abs(curX)
y = abs(curY)

y1 = int( x + y )
x1 = y1
area = x1 * x1
newA = area

while newA <= area:
    x1, y1 = x1 + 1, x1 + 1
    area = newA
    newA = x1 * x1


x1 = int((x1-1) * (curX / abs(curX)))
y1 = int((y1-1) * (curY / abs(curY)))

if x1 < 0 :
    print(str(x1) + ' 0 0 ' + str(y1))
else:
    print('0 ' + str(y1) + ' ' + str(x1) + ' 0')


