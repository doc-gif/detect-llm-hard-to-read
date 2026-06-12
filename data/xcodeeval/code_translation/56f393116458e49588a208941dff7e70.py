x, y, z =  map(int, input().split())


a, b, c = map(int, input().split())

n = True
if x <= a and (x + y) <= (a + b) and (x + y + z) <= (a + b + c):
    n = False
if n:
    print('NO')
else:
    print("YES")
