from itertools import permutations
 
n,k = map(int,input().split())
a = []
mn = float("inf")
for _ in range(n):
    line = input()
    a.append(list(permutations(line)))
 
for arr in zip(*a):
    ints = [int(''.join(num)) for num in arr]
    mn = min(mn,max(ints)-min(ints))
 
print(mn)