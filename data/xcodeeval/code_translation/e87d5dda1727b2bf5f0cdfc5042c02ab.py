x, y = map(int, input().split(" "))
k = 0
if(y % x != 0):
    print(-1)
else:
    y = y / x
    while y != 1:
        if(y % 2 == 0):
            y /= 2
            k += 1
        elif(y % 3 == 0):
            y /= 3
            k += 1
        else:
            print(-1)
            break
    else: print(k)           
