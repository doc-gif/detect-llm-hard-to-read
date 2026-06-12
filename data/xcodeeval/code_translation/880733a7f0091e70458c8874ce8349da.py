n = input().split()
if n[2] == 'week':
    print(53 if int(n[0]) == 5 or int(n[0]) == 6 else 52)
else:
    if int(n[0]) == 31:
        print(7)
    elif int(n[0]) == 30:
        print(11)
    else:
        print(12)
