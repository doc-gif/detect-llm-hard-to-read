n = int(input())
s = list(input())
i = 1
total = 0
if n == 1:
    print(1)
else:
    while i < n:
        if (s[i-1] + s[i] == "UU") or (s[i-1] + s[i] == "RR"):
            total += 1
            i += 1
        elif (s[i-1] + s[i] == "UR") or (s[i-1] + s[i] == "RU"):
            total += 1
            i += 2
        if i == n:
            total += 1
    print(total)

