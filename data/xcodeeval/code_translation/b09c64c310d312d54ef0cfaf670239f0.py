u = [0]*10000
a = int(input())
b = input().split()
start = int(b[0])
me = int(b[0])
mx = 0
for i in b[1:]:
    i = int(i)
    u[i]+=1
    mx=max(mx,i)
i = mx
while me<i:
    z = u[i]
    while u[i] and me<=i:
        me+=1
        u[i]-=1
    u[i-1]+=z
    i-=1
if me == i:
    me+=1
print(me-start)
