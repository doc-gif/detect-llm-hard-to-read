n = int(input())
a = ["","",""]
for i in range(n):
    l = input()
    a[i] = l.split();
    for j in range(6):
        a[i][j] = int(a[i][j])

x = 1;
while(x<=9):
    it = 0
    i = 0
    while i<n:
        j = 0
        while j < 6:
            if a[i][j] == x:
                x = x + 1
                it = 1
                break
            j = j + 1
        if it == 1:
            break
        i = i + 1
    if it == 0:
        break
while ( 9 < x < 100):
    it = 0
    i = 0
    while i < 6:
        j = 0
        while j < 6:
            if n > 0 and a[0][i]*10 + a[1][j] == x:
                x = x + 1
                it = 1
                break
            if n > 0 and a[1][i]*10 + a[0][j] == x:
                x = x + 1
                it = 1
                break
            if n > 1 and a[0][i]*10 + a[2][j] == x:
                x = x + 1
                it = 1
                break
            if n > 1 and a[2][i]*10 + a[0][j] == x:
                x = x + 1
                it = 1
                break
            if n > 1 and a[1][i]*10 + a[2][j] == x:
                x = x + 1
                it = 1
                break
            if n > 1 and a[2][i]*10 + a[1][j] == x:
                x = x + 1
                it = 1
                break
            j = j + 1
        if it==1:
            break
        i = i + 1
    if it == 0:
        break
while ( 99 < x < 1000):
    it = 0
    i = 0
    while i < 6:
        j = 0
        while j < 6:
            k = 0
            while k < 6:                
                if n > 1 and a[0][i]*100 + 10*a[1][j] + a[2][k] == x:
                    x = x + 1
                    it = 1
                    break
                k = k + 1
            if it == 1:
                break
            j = j + 1
        if it == 1:
            break
        i = i + 1
    if it == 0:
        break
print (x - 1)
