n = int(input())
s = list(map(int, input().split()))
a = 0
for i in range(n+1):
    x = s[:i].count(0)
    y = s[i:].count(1)
    a = max(a, x+y)
print(a)