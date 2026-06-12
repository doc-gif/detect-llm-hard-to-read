s1 = raw_input()
s2 = raw_input()
sm1 = 0
for ch in s1:
    if ch == "+":
        sm1 += 1
    else:
        sm1 -= 1
if "?" not in s1 and "?" not in s2:
    sm2 = 0
    for ch in s2:
        if ch == "+":
            sm2 += 1
        else:
            sm2 -= 1
    print(1 if sm1 == sm2 else 0)
    exit()
make2 = [s2]
while any("?" in seq for seq in make2):
    next_gen = []
    for seq in make2:
        if "?" not in seq:
            continue
        for j in range(len(seq)):
            if seq[j] == "?":
                next_gen.append(seq[:j] + "-" + seq[j + 1 :])
                next_gen.append(seq[:j] + "+" + seq[j + 1 :])
                break
    make2 = next_gen


def calc_sum(s):
    total = 0
    for ch in s:
        if ch == "+":
            total += 1
        else:
            total -= 1
    return total


make2 = [calc_sum(seq) for seq in make2]
matches = sum(1 for val in make2 if val == sm1)
print(matches * 1.0 / len(make2))
