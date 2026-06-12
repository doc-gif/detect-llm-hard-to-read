first=0
second=0
draw=0
z,x=list(map(int,input().split()))
for i in range(1,7):
    #print('(i-z)=%d   (i-x)=%d'%(abs(i-z),abs(i-x)))
    if abs(i-z)<abs(i-x):
        first+=1
      #  print('first',first)
    elif abs(i-z)>abs(i-x) :
        second+=1
       # print('second',second)
    else:
      draw+=1
     # print('draw',draw)
print(first,draw,second)  