n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
ans = 0
for i in range(1, 6):
    x, y = a.count(i), b.count(i)
    if (x+y) & 1:
        ans = -1
        break
    ans += abs(x - y) // 2
print(ans//2)
