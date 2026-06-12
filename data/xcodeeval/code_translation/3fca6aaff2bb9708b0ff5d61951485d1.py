k, s = 1, input()

for i in range(len(s)-1):
    if s[i] != s[i+1]:
        k = 0
    elif k >= 6:
        break
    k += 1

print("NO" if k < 6 else "YES")
