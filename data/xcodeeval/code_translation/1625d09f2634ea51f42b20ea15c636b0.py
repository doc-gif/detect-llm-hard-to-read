n, k, d = map(int, input().split())
k = n if n<k else k
cnt = [0 for _ in range(n+1)]
cn = [0 for _ in range(n+1)]
cnt[0] = cn[0] = 1
for i in range(1,n+1):
    for j in range(1,k+1):
        if i>=j:
            cnt[i] += cnt[i-j]
        if i>=j and j<d:
            cn[i] += cn[i-j]
s1 = cnt[n]
s2 = cn[n]
print((s1-s2)%1000000007)