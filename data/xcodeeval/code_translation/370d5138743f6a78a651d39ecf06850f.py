arr=[]
arr1=[]
arr2=[]
for i in range(0,4):
    x1,y1,x2,y2=map(int,input().split())
    p1=(x1,y1)
    p2=(x2,y2)
    p3=(x1,y1,x2,y2)
    arr2.append(p3)
    arr.append(p1)
    arr.append(p2)
arr1=list(set(arr))
if len(arr1)>4 or len(arr1)<4:
    print("NO")
    exit()
minx=10000000000
maxx=-10000000000
miny=10000000000
maxy=-10000000000
for i in range(0,len(arr1)):
    if minx>arr1[i][0]:
        minx=arr1[i][0]
    if maxx<arr1[i][0]:
        maxx=arr1[i][0]
    if miny>arr1[i][1]:
        miny=arr1[i][1]
    if maxy<arr1[i][1]:
        maxy=arr1[i][1]
arr3=[]
arr3.append((minx,miny,maxx,miny))
arr3.append((maxx,miny,maxx,maxy))
arr3.append((maxx,maxy,minx,maxy))
arr3.append((minx,maxy,minx,miny))
# print(arr3)
count=0
for i in range(0,4):
    for j in range(0,4):
        if arr3[i][0]==arr2[j][0] and arr3[i][1]==arr2[j][1] and arr3[i][2]==arr2[j][2] and arr3[i][3]==arr2[j][3]:
            count+=1
            break
            # print(arr3[i][0],arr3[i][1],arr3[i][2],arr3[i][3],arr2[i][0],arr2[i][1],arr2[i][2],arr2[i][3])
        elif arr3[i][2]==arr2[j][0] and arr3[i][3]==arr2[j][1] and arr3[i][0]==arr2[j][2] and arr3[i][1]==arr2[j][3]:
            count+=1
            break
            # print(arr3[i][0],arr3[i][1],arr3[i][2],arr3[i][3],arr2[i][0],arr2[i][1],arr2[i][2],arr2[i][3])
# print(count)
# print(arr2,arr3)
if count==4:
    print("YES")
else:
    print("NO")
