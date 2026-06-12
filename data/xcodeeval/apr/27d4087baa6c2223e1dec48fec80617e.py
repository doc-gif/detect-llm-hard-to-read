a, b = map(int, input().split())
if a == b:
    print(0)
else:
    a2 = 0
    a3 = 0
    a5 = 0
    while True:
        if a % 2 == 0:
            a = a // 2
            a2 += 1
        elif a % 3 == 0:
            a = a // 3
            a3 += 1
        elif a % 5 == 0:
            a = a // 5
            a5 += 1
        else:
            break
    b2 = 0
    b3 = 0
    b5 = 0
    while True:
        if b % 2 == 0:
            b = b // 2
            b2 += 1
        elif b % 3 == 0:
            b = b // 3
            b3 += 1
        elif b % 5 == 0:
            b = b // 5
            b5 += 1
        else:
            break
    if a != b:
        print(-1)
    else:
        print(abs(a2 - b2) + abs(a3 - b3) + abs(a5 - b5))