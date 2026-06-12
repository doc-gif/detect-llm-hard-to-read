import math
r,g,b=map(int,input().split(" "))
li = [r,g,b]
li.sort()
if(li[2]>2*(sum(li)-li[2])):
    print(sum(li)-li[2])
else:
    print(sum(li)//3)
