x, y = map(int, input().split())
distance = (x**2 + y**2) ** 0.5
if distance == int(distance):
    print("black")
elif (x < 0 and y < 0) or (x > 0 and y > 0):
    if int(distance) % 2 == 0:
        print("black")
    else:
        print("white")
else:
    if int(distance) % 2 != 0:
        print("black")
    else:
        print("white")