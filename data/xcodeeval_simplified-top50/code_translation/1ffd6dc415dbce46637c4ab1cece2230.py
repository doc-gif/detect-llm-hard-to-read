x, y = map(int, input().split())
a = 1
b = 0
if y == 0:
    print("No")
elif y == 1:
    print("Yes" if x == 0 else "No")
else:
    b += y - a
    if b > x:
        print("No")
    elif b == x:
        print("Yes")
    else:
        temp = x - b
        print("Yes" if temp % 2 == 0 else "No")