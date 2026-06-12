p, x, y = map(int, input().split())
Tshirt = []
hk = 0
suchk = 0
while x < y:
    hk += 1
    x += 100


def genT():
    Tshirt.clear()
    s = x
    i = (s // 50) % 475
    for _ in range(25):
        i = (i * 96 + 42) % 475
        Tshirt.append(26 + i)


genT()
if p in Tshirt:
    print(suchk)
    exit(0)
orgx = x
while x >= y:
    x -= 50
    genT()
    if p in Tshirt:
        print(suchk)
        print("f")
        exit(0)
x = orgx
while p not in Tshirt:
    hk += 1
    if hk % 2 == 1:
        suchk += 1
    x += 50
    genT()
print(suchk)
