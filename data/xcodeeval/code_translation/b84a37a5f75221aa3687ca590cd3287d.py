a = input()
ans = 0
i = 0
while i < len(a):
    j = i + 1
    while j < len(a) and a[j] == a[i] and j - i < 5: j+=1
    ans+=1
    i = j
print(ans)