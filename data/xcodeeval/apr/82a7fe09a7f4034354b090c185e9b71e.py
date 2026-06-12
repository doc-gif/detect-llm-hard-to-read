n, m = map(int, input().split())
a1, s1 = list(map(int, input().split())), list(map(int, input().split()))
a2, s2, a, s = [], [], [], []
for q in range(0, n*2, 2):
    a2.append([a1[q], a1[q+1]])
for q in range(0, m*2, 2):
    s2.append([s1[q], s1[q + 1]])
for q in range(n):
    k = set()
    for q1 in range(m):
        if len(set(a2[q]) & set(s2[q1])) == 1:
            k.add(list(set(a2[q]) & set(s2[q1]))[0])
    if k:
        a.append([a2[q][0], a2[q][1], list(k)])
for q in range(m):
    k = set()
    for q1 in range(n):
        if len(set(s2[q]) & set(a2[q1])) == 1:
            k.add(list(set(s2[q]) & set(a2[q1]))[0])
    if k:
        s.append([s2[q][0], s2[q][1], list(k)])
z, p = set(), float('inf')
for q in range(len(a)):
    if len(a[q][2]) > 1:
        print(-1)
        p = -1
        break
    z.add(a[q][2][0])
else:
    if len(z) > 1:
        p = 1
    z = set()
    for q in range(len(s)):
        if len(s[q][2]) > 1:
            print(-1)
            p = -1
            break
        z.add(a[q][2][0])
    else:
        if len(z) > 1 or p == 1:
            print(0)
        else:
            print(list(z)[0])
