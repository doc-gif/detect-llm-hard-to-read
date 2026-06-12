a = input().split()
b = [[], [], []]
t = [0, 0, 0]
suits = ["m", "p", "s"]
for i in range(3):
    if a[i][1] == suits[0]:
        b[0].append(int(a[i][0]))
        t[0] += 1
    elif a[i][1] == suits[1]:
        b[1].append(int(a[i][0]))
        t[1] += 1
    else:
        b[2].append(int(a[i][0]))
        t[2] += 1
max_t = max(t)
if max_t == 3:
    i = 0
    while i < 3:
        if t[i] == 3:
            break
    diffs = []
    diffs.append(abs(b[i][1] - b[i][0]))
    diffs.append(abs(b[i][1] - b[i][2]))
    diffs.append(abs(b[i][2] - b[i][0]))
    diffs.sort()
    if diffs[0] <= 2:
        if diffs == [0, 0, 0] or diffs == [0, 1, 2]:
            print(0)
        else:
            print(1)
    else:
        print(2)
if max_t == 2:
    i = 0
    while i < 3:
        if t[i] == 2:
            break
        i += 1
    if abs(b[i][1] - b[i][0]) <= 2:
        print(1)
    else:
        print(2)
if max_t == 1:
    print(2)
