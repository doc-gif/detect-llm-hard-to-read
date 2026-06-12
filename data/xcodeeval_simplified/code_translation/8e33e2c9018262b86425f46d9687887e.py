def compute_f_values(limit):
    f = [0] * limit
    for n in range(1, limit):
        f[n] = 2 ** (n - 1) + 2 * f[n - 1]
    return f
f_values = compute_f_values(60)
n = int(input())
ans = 0
for k in range(59, -1, -1):
    if n >= 2**k:
        ans += f_values[k]
        n -= 2**k
        if n > 0:
            ans += 2**k
print(ans)