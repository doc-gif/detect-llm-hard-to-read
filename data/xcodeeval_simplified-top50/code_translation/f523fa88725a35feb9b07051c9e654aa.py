def check(s, i):
    if i == len(s):
        x = "".join(s)
        if x[0] == "0" and x != "0":
            return 0
        if int(x) % 25 == 0:
            return 1
        return 0
    res = 0
    if s[i] == "_":
        if i != 0 and i < len(s) - 2:
            s[i] = "1"
            res += 10 * check(s, i + 1)
        else:
            for j in range(10):
                s[i] = str(j)
                res += check(s, i + 1)
        s[i] = "_"
        return res
    else:
        return check(s, i + 1)
inp = input()
total = 0
if "X" in inp:
    for i in range(10):
        s = inp.replace("X", str(i))
        total += check(list(s), 0)
else:
    total = check(list(inp), 0)
print(total)