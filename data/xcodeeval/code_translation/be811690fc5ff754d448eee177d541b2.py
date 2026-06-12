import math
x=eval(input())
y=math.sqrt(x)
if y%1==0:
  y=y
elif y%1>=0.5:
  y=(y//1)+1
else:
  y=(y//1)+0.5
print(int(2*y))

