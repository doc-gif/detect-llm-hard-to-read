a, b, c = map(int, input().split())
if a > b:
    while c >= 0 and c % a != 0:
        c -= b
else:
    while c >= 0 and c % b != 0:
        c -= a
print("No" if c < 0 else "Yes")