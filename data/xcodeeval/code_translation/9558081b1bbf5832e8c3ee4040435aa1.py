n,m = map(int, input().split())
matches = {}
count = 0
for i in range(m):
    j,k = map(int, input().split())
    repeated = 0
    for e in matches.keys():
        if e == k:
            repeated = 1
            matches[k] += j
    if repeated == 0:
        matches[k] = j
while n > 0 and len(matches) != 0:
    biggest = max(matches.keys())
    times = min(n, matches[biggest])
    count += times*biggest
    matches[biggest] -= times
    if matches[biggest] == 0:
        matches.pop(biggest)
    n -= times

print(count)