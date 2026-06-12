b, d = map(int, input().split())
for i in range(1, 10):
    if (b**i) % d == 0:
        print("2-type")
        print(i)
        exit()
if (b-1) % d == 0:
    print("3-type")
    exit()
if (b+1) % d == 0:
    print("11-type")
    exit()
for i in range(2, d+1):
    if d % i == 0:
        x = 1
        while d % i == 0: 
            d /= i 
            x *= i
        if (b**10) % x != 0 and (b+1) % x != 0 and (b-1) % x != 0:
            print("7-type")
            break
else:
    print("6-type")
