p, y = map(int, input().split())
ans = -1
for candidate in range(y, p, -1):
    divisor = candidate
    i = 2
    while i * i <= candidate:
        if candidate % i == 0:
            divisor = i
            break
        i += 1
    if divisor > p:
        ans = candidate
        break
print(ans)