a, b = map(int, input().split())
x = a - b
x = str(x)
while len(x) < len(str(a)):
    x = '0' + x
pos = 0
for i in range(len(str(a)) - 1, -1, -1):
    y = x
    x = x[:i] + '9' + x[i + 1:]
    if int(x) > a:
        pos = i
        break
x = y
for i in range(pos + 1):
    for j in range(10 - int(x[i])):
        y = x
        x = x[:i] + str(int(x[i]) + 1) + x[i + 1:]
        if int(x) > a:
            break
    x = y
print(int(x))