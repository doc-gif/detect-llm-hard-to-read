n , m = map(int,input().split())
l = list(map(int,input().split()))
a = []

for i in range(1,n+1):
    for j in l :
        if j <= i :
            a.append(j)
            break

print(*a)




