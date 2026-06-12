n, m = map(int, input().split())
ans = 0
fact = [1] * (n + 1)
for i in range(1, n + 1):
    fact[i] = fact[i - 1] * i
for d in range(1, n):
    s = n - d
    t = fact[d + 1] * fact[n - d - 1] * s * (n - d)
    ans = (ans + t) % m
temp = fact[n] * n
ans = (ans + temp) % m
print(ans)
