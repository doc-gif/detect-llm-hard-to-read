n = input().split()
r = int(n[0]) % 10
c = int(n[1])

for i in range(1,10):
    if (((i * r) - c) % 10 == 0) or (((i * r)) % 10 == 0):
        print(i)
        break
        