s = input()
n = int(input())

l, r = [-1e9] * 101, [-1e9] * 101
l[0] = r[0] = 0

for q in s:
    for j in range(n, -1, -1):
        x = max(r[j], l[j - 1] + 1) if q == 'T' else max(l[j] + 1, r[j - 1])
        y = max(l[j], r[j - 1] + 1) if q == 'T' else max(r[j] - 1, l[j - 1])
        l[j], r[j] = x, y

print(max(l[n % 2:n + 1:2] + r[n % 2:n + 1:2]))
