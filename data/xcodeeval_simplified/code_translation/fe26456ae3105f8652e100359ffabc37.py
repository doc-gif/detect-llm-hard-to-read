c, a, b = map(int, input().split())
level = 0
while c != 1:
    level += 1
    c //= 2
a -= 1
b -= 1
roundik = 0
while a != b:
    roundik += 1
    a //= 2
    b //= 2
print("Final!" if roundik == level else roundik)