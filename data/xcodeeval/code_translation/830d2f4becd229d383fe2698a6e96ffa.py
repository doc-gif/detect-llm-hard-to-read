INF = 10000
n = input()
ans = INF
k = len(n)
for i in range(k):
    for j in range(k):
        if i == j:
            continue
        s = n
        tmp = 0
        for p in range(i, k - 1):
            s = s[:p] + s[p + 1] + s[p] + s[p + 2:]
            tmp += 1
        for p in range(j - (j > i), k - 2):
            s = s[:p] + s[p + 1] + s[p] + s[p + 2:]
            tmp += 1
        pos = -1
        for p in range(k):
            if s[p] != '0':
                pos = p
                break
        for p in range(pos, 0, -1):
            s = s[:p - 1] + s[p] + s[p - 1] + s[p + 1:]
            tmp += 1
        if int(s) % 25 == 0:
            ans = min(ans, tmp)
print(ans if ans != INF else -1)
