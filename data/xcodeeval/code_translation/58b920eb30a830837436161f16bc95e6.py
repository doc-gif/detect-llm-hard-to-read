import sys
input = sys.stdin.readline
I = lambda : map(int,input().split())

n,m,k = I()
l = list(I())

l.sort(reverse = True)

count = 0 

if k >= m:
    count = 0
else:
    for i in range(n):
        count += 1
        k += (l[i] -1)
        if k  >= m: #count = good
            break
        if (k== 0 or l[i] == 1) or k == 0: #ended without having good count
            count = -1
            break
        
    if k < m:
        count = -1
    
print(count)   