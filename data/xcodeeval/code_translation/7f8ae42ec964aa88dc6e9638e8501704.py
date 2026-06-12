n = int(input())
s = input()
ans = 0
for i in range(n, 2, -1):
    st = 'x'*i
    while s.count(st):
        ans += s.count(st)*(i-2)
        s = s.replace(st, '')
print(ans)