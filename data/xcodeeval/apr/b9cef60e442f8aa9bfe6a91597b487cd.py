import sys,math
from collections import defaultdict
from io import BytesIO

sys.stdin = BytesIO(sys.stdin.read())
input = lambda: sys.stdin.readline().rstrip('\r\n')
n = int(input())
#n,q = [int(x) for x in input().split(' ')]
arr = [int(x) for x in input().split(' ')]
#sec = [set()] * n
basen = n
while n > 100:
    if sum(arr) == 0:
        break
    dif = n - 100
    for i in range(8,0,-1):
        if arr[i-1] > 0:
            n -= i * min(dif // i + 1, arr[i-1])
            arr[i-1] -= min(dif // i + 1, arr[i-1])
            break

cur = 0
dot8 = set()
while cur <= n and arr[-1] >= 0:
    arr[-1] -= 1
    dot8.add(cur)
    cur += 8

cur = 0
dot7 = set()
while cur <= n and arr[-2] >= 0:
    arr[-2] -= 1
    dot7.add(cur)
    cur += 7
    
cur = 0
dot6 = set()
while cur <= n and arr[-3] >= 0:
    arr[-3] -= 1
    dot6.add(cur)
    cur += 6
    
cur = 0
dot5 = set()
while cur <= n and arr[-4] >= 0:
    arr[-4] -= 1
    dot5.add(cur)
    cur += 5
    
cur = 0
dot4 = set()
while cur <= n and arr[-5] >= 0:
    arr[-5] -= 1
    dot4.add(cur)
    cur += 4
    
cur = 0
dot3 = set()
while cur <= n and arr[-6] >= 0:
    arr[-6] -= 1
    dot3.add(cur)
    cur += 3
    
cur = 0
dot2 = set()
while cur <= n and arr[-7] >= 0:
    arr[-7] -= 1
    dot2.add(cur)
    cur += 2
#print(n,dot8,dot7)

resdot = set()
newdot = set()
for el8 in dot8:
    for el7 in dot7:
        if el8 + el7 <= n:
            resdot.add(el8+el7)
for el6 in dot6:
    for el in resdot:
        if el6 + el <= n:
            newdot.add(el6+el)
resdot = newdot
newdot = set()
for el5 in dot5:
    for el in resdot:
        if el5 + el <= n:
            newdot.add(el5+el)
resdot = newdot
newdot = set()
for el4 in dot4:
    for el in resdot:
        if el4 + el <= n:
            newdot.add(el4+el)
resdot = newdot
#print(newdot)
newdot = set()
for el3 in dot3:
    for el in resdot:
        if el3 + el <= n:
            newdot.add(el3+el)
resdot = newdot
#print(resdot,newdot,dot2)
newdot = set()
for el2 in dot2:
    for el in resdot:
        if el2 + el <= n:
            newdot.add(el2+el)
#print(newdot)
m = max(newdot)
print(basen + m - n + (min(n-m,arr[0])))
