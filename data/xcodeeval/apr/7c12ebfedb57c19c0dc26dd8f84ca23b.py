n = int(input())
f = []
X = []
Y = []
for i in range(4 * n + 1):
    x, y = map(int, input().split())
    f.append((x, y))
    X.append(x)
    Y.append(y)
l = min(X)
r = max(X)
d = min(Y)
u = max(Y)
if r - l == u - d:
    for i in f:
        if X.count(i[0]) == 1 and Y.count(i[1]) == 1:
            print(i[0], i[1])
            break
    for i in f:
        if l < i[0] < r and d < i[1] < u:
            print(i[0], i[1])
            break
else:
    for i in f:
        if X.count(i[0]) == 1 and Y.count(i[1]) == 1:
            print(i[0], i[1])
            break
    for i in f:
        if X.count(i[0]) == 1 and (i[0] == l or i[0] == R):
            print(i[0], i[1])
            break
        elif Y.count(i[1]) == 1 and (i[1] == u or i[1] == d):
            print(i[0], i[1])
            break
