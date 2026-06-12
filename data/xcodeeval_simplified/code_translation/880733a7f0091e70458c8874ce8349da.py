n = input().split()
day, unit = int(n[0]), n[2]
if unit == "week":
    print(53 if day == 5 or day == 6 else 52)
else:
    if day == 31:
        print(7)
    elif day == 30:
        print(11)
    else:
        print(12)