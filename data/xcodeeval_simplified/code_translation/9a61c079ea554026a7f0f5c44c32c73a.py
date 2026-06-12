a, b = map(int, input().split())
i = 1
while True:
    if i % 2:
        if a < i:
            print("Vladik")
            break
        a -= i
    else:
        if b < i:
            print("Valera")
            break
        b -= i
    i += 1