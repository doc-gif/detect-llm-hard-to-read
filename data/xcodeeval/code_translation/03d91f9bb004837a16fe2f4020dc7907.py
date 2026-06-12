n = int(input())
p = 1
pp = 0
if (n % 400 == 0) or ((n % 4 == 0) and (n % 100 != 0)):
    pp = 4
else:
    pp = 1
for i in range (n + 1, n + 100):
    if (i % 400 == 0) or ((i % 4 == 0) and (i % 100 != 0)):
        p += 2
    else:
        p += 1
    p %= 7
    if (p == 1) and (pp == 4) and ((i % 400 == 0) or ((i % 4 == 0) and (i % 100 != 0))):
        print(i)
        break
    elif (p == 1) and (pp == 1) and ((i % 4 != 0) or ((i % 4 == 0) and (i % 100 == 0))):
        print(i)
        break