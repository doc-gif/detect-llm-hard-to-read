n = input()
s = input()
s = ''.join(reversed(sorted(s)))
if s == '0':
    print(0)
    exit(0)
k = 0
for i in range(len(s)):
    if s[i] == '0':
        k += 1
if n == 1:
    print(s)
    exit(0)
ans = '1' + '0'*k
print(ans)
