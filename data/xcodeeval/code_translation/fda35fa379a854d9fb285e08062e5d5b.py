a = int(input())
summ = 5
while summ % 4 != 0:
    summ = 0
    a = str(a)
    for i in a:
        summ += int(i)
    if summ % 4 != 0:
        a = int(a) + 1
print(a)

