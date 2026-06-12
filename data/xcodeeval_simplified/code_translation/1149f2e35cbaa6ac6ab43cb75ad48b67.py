s = input().strip()
j = 4 if s[0] == "h" else 3
i = j
found_ru = False
while i < len(s):
    if found_ru and s[i] == "r" and s[i + 1] == "u":
        break
    i += 1
    found_ru = True
if i + 2 == len(s):
    print(s[:j] + "://" + s[j:i] + ".ru")
else:
    print(s[:j] + "://" + s[j:i] + ".ru/" + s[i + 2 :])