ax,ay,bx,by,cx,cy=map(int,input().split())
if (ax-bx)**2+(ay-by)**2==(cx-bx)**2+(cy-by)**2 and ((ax+cx)/2!=bx or (ay+cy)/2!=by):print("Yes")
else:print("No")