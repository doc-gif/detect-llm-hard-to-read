n,m,r = map(int, input().split())
s = [int(x) for x in input().split()]
b = [int(x) for x in input().split()]
s.sort()
bm = max(b)

poc = 0
i = 0
while r > 0 and i < n:
    za_kolko = s[i]
    if za_kolko >= bm:
        break
    k = r//za_kolko
    poc += k
    r %= za_kolko
    i += 1

print(poc*bm + r)
