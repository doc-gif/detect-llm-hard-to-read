n, m = map(int, input().split())
b = []
for t in range(n):
    a = input()
    s = [char for char in a]
    b.append(s)
    
i = 0
j = 0

while i < n:
    while j < m:
        if b[i][j] == "S":
            break
        if j+1 == m:
            j = 0
            while j < m:
                b[i][j] = "X"
        j+=1
    j = 0
    i+=1
        
i = 0
j = 0
while j < m:
    while i < n:
        if b[i][j] == "S":
            break
        if i+1 == n:
            i = 0
            while i < n:
                b[i][j] = "S"    
        i+=1
    i = 0
    j+=1
total = 0
for c in range(len(b)):
    for l in range(len(b[c])):
        if b[c][l] == "X":
            total+=1
total = 0 