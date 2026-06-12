import math
r,x1,y1,x2,y2=[int(x) for x in input().split()]
ans=(math.sqrt((x2-x1)**2+(y2-y1)**2))/(2*r)
ans=int(math.ceil(ans))
print(ans)


