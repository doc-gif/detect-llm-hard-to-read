n = int(input())
a = []
i = 1
s = 0
while i ** 2 <= n:
    if n % i == 0:
        a.append(i)
        a.append(n // i)
    i = i + 1
a = set(a)
for i in a:
    oth = {'1', '2', '3', '5', '6', '8', '9', '0'}
    if oth == oth - (set(str(i))):
        s = s + 1
if s > 0:
    print('YES')
else:
    print('NO')
