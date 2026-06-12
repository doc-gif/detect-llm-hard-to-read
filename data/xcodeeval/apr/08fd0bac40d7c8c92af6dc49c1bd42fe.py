n, m, nomber = map(int, input().split())
a = []
for i in range(m):
    a.append([0]*n*2)
    
x1 = 1
x2 = 2
for j in range(0, n*2-1, 2):
    a[0][j] = x1
    a[0][j+1] = x2
    x1 = x1 + m*2
    x2 = x2 + m*2

x = 0 
y = 0 
for i in range(1, m):
    for j in range(n*2):
        a[i][j] = a[i-1][j] + 2

for i in range(m):
    for j in range(n*2):
        if (a[i][j] == nomber):
            x = i #номер ряда
            y = j #как бы номер парты
            break
x = x + 1 
if y % 2 == 0:
    y = y / 2
    vector = 'L'
elif y % 2 != 0:
    y = y // 2
    vector = 'R'
y = int(y) + 1
"""
for row in a:
    print(' '.join([str (elem) for elem in row]))
"""
#print(a[2][4])
print(y, x, vector)




        
