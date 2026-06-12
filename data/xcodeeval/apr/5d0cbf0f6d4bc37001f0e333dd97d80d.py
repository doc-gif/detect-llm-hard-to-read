from collections import defaultdict
#n = int(raw_input())
n,b = [int(x) for x in raw_input().split()]
#arr = [int(x) for x in raw_input().split()]

s = 0
d_osn = defaultdict(int)
while b > 1:
    for i in range(2,b):
        if b % i == 0:
            d_osn[i] += 1
            b /= i
            break
    else:
        d_osn[b] += 1
        b = 1
#print(d_osn)
izv = defaultdict(int)
for i in range(1,n+1):
    for el in d_osn:
        while i % el == 0:
            i = i / el
            izv[el] += 1
res = -1
#print(izv)
for k in d_osn:
    mlt = 0 if k not in izv else izv[k] // d_osn[k]
    if res == -1:
        res = mlt
    elif mlt < res:
        res = mlt
print(res)