n, x = map(int, input().split())
l = list(map(int, input().split()))
missing = [i for i in range(max(max(l) + 2, x)) if i not in l]
if x in missing:
    d = sum(1 for i in missing if i < x)
else:
    if max(l) + 2 > x:
        d = sum(1 for i in missing if i < x) + 1
    else:
        d = len(missing)

print(d)
