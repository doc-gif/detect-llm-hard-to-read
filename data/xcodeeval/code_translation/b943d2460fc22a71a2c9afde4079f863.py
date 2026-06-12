f = input()
m = input()
s = input()
diction = dict()
diction2 = dict()

diction["F"] = f
diction["M"] = m
diction["S"] = s

for value in diction.values():
    diction2[value] = diction2.get(value, 0) + 1


if f == m and f == s:
    print("?")
elif f != m and f != s and m != s:
    print("?")
else:
    if "scissors" not in diction.values():
        if diction2["paper"] > 1:
            print("?")
        else:
            for val in diction:
                if diction[val] == "paper":
                    print(val)
    elif "paper" not in diction.values():
        if diction2["rock"] > 1:
            print("?")
        else:
            for val in diction:
                if diction[val] == "rock":
                    print(val)
    elif "rock" not in diction.values():
        if diction2["scissors"] > 1:
            print("?")
        else:
            for val in diction:
                if diction[val] == "scissors":
                    print(val)