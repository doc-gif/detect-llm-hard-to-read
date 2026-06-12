'''
二维数组转置,排序,lambda表达式函数
'''

mylist = [list(map(int, input().split())),list(map(int, input().split()))]
mylist = list(map(list,zip(*mylist)))
for my in  mylist:
    if my[0]<my[1]:
        my[1]-=my[0]
        my[0]=0
    else:
        my[0]-=my[1]
        my[1]=0
# for i in range(len(mylist)):
#     if mylist[i][0]<mylist[i][1]:
#         mylist[i][1]-=mylist[i][0]
#         mylist[i][0]=0
#     else:
#         mylist[i][0]-=mylist[i][1]
#         mylist[i][1]=0
mylist.sort(key=lambda my:my[0], reverse=True)
i=0 #初始剩余资源
j=0 #目标资源量
while j<3 and i<3:
    while mylist[j][1]>0 and i<3:
        if mylist[i][0]<=mylist[j][1]*2:
            mylist[j][1]-=mylist[i][0]//2
            i+=1
        else:
            mylist[i][0]-=mylist[j][1]*2
            mylist[j][1]=0
    j+=1
if mylist[2][1]+mylist[1][1]+mylist[0][1]>0:
    print("No")
else:
    print("Yes")
     
     
         