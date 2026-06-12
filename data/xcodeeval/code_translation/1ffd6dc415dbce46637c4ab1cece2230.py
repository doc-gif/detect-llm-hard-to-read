x,y = list(map(int,input().split()))
a = 1
b = 0
if y == 0:
    print("No")
elif y == 1:
    if x == 0:
        print("Yes")
    else:
        print("No")
else:
    b += y - a
    if b > x:
        print("No")
    elif b == x:
        print("Yes")
    else:
        temp = x - b
        if temp % 2 == 0:
            print("Yes")
        else:
            print("No")