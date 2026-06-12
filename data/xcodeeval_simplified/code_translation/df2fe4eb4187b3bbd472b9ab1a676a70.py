mylist = [list(map(int, input().split())), list(map(int, input().split()))]
mylist = list(map(list, zip(*mylist)))
for pair in mylist:
    if pair[0] < pair[1]:
        pair[1] -= pair[0]
        pair[0] = 0
    else:
        pair[0] -= pair[1]
        pair[1] = 0
mylist.sort(key=lambda p: p[0], reverse=True)
i = 0
j = 0
while j < 3 and i < 3:
    while mylist[j][1] > 0 and i < 3:
        if mylist[i][0] <= mylist[j][1] * 2:
            mylist[j][1] -= mylist[i][0] // 2
            i += 1
        else:
            mylist[i][0] -= mylist[j][1] * 2
            mylist[j][1] = 0
    j += 1
if mylist[2][1] + mylist[1][1] + mylist[0][1] > 0:
    print("No")
else:
    print("Yes")