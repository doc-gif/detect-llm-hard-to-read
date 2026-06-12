n, k = map(int, input().split())
a = input()
a = a.lower()
f = [0] * 26
for i in a:
    f[ord(i) - 97] += 1
if max(f) > k:
    print("NO")
else:
    print("YES")
