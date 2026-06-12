p, y = map(int, input().split())

ans = -1

for j in range(y, p, -1):
    i = 2
    d = j
    while i * i <= j:
        if j % i == 0:
            d = i
            break
        i += 1

    if d > p:
        ans = j
        break

print(ans)        
        
    


