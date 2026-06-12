import sys
import math

n = int(sys.stdin.readline())

v = [0] * n
ost = 1
if(n > 1):
    v[1] = 1
for i in range(1, n + 1):
    ost = (ost + i) % n
    v[ost] = 1

for i in v:
    if(i == 0):
        print("NO")
        exit()
    
print("YES")
    
    