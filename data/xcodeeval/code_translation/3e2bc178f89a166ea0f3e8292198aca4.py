x = input().lower()
y = input().lower()
count, z = 0, 0
for i in range(z, len(x)):
    for j in range(z, len(y)):
        if ord(x[i]) == ord(y[j]):
            z += 1
        if ord(x[i]) < ord(y[j]) and count != 1:
            count = -1

        if ord(x[i]) > ord(y[j]) and count != -1:
            count = 1
        break

print(count)