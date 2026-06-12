from collections import Counter

s1 = input()
s2 = input()
c1 = Counter(s1)
c2 = Counter(s2)
have2 = have5 = have6 = have9 = 0
if c1["2"] and c1["5"]:
    total_25 = c2["2"] + c2["5"]
    a, b = c1["2"], c1["5"]
    have2 = a / b * total_25
    have5 = b / a * total_25
elif c1["2"] or c1["5"]:
    have2 = have5 = c2["2"] + c2["5"]
if c1["6"] and c1["9"]:
    total_69 = c2["6"] + c2["9"]
    a, b = c1["6"], c1["9"]
    have6 = a / b * total_69
    have9 = b / a * total_69
elif c1["6"] or c1["9"]:
    have6 = have9 = c2["6"] + c2["9"]
mini = 10**9
for digit in c1:
    if digit not in "2569" and c1[digit]:
        mini = min(mini, c2[digit] // c1[digit])
if c1["2"]:
    mini = min(mini, have2 // c1["2"])
if c1["5"]:
    mini = min(mini, have5 // c1["5"])
if c1["6"]:
    mini = min(mini, have6 // c1["6"])
if c1["9"]:
    mini = min(mini, have9 // c1["9"])
print(mini if mini != 10**9 else 0)
