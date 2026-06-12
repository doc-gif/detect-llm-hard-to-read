n, k = map(int, input().split())
s = input()
max_n_len = 0
left = 0
while left < n:
    if s[left] != "N":
        left += 1
    else:
        right = left + 1
        while right < n and s[right] == "N":
            right += 1
        max_n_len = max(max_n_len, right - left)
        left = right
if max_n_len > k:
    print("NO")
    exit(0)
ans = "NO"
for start in range(n):
    can = 1
    if start + k < n and s[start + k] == "N":
        can = 0
    if start == 0 or s[start - 1] != "N":
        if start + k <= n:
            for i in range(k):
                if s[start + i] == "Y":
                    can = 0
    else:
        can = 0
    if can == 1:
        ans = "YES"
print(ans)
