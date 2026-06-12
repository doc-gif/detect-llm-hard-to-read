a, b, c = map(int, input().split())
if a > b:
    while c % a != 0 and c >= 0:
        c -= b
else:
    while c % b != 0 and c >= 0:
        c -= a
if c < 0:
    print("No")
else:
    print("Yes")