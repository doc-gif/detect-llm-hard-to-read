from collections import deque

def lastTwo(s):
    if s == "__":
        return 4
    elif s[0] == "_":
        return 2 if s[1] == "0" or s[1] == "5" else 0#(1 if s[1] == "2" or s[1] == "7" else 0)
    elif s[1] == "_":
        return int(s[0] == "0" or s[0] == "2" or s[0] == "5" or s[0] == "7")
    else:
        return int(int(s) % 25 == 0)
    # return (4 if current[-2:] == "__" else (1 if (current[-1] == "_" and )))

def sPossibleCount(s):
    if "X" in s:
        start = int(s[0] == "X")
        q = ["".join([s[i] if s[i]!="X" else str(x) for i in range(len(s))]) for x in range(start, 10)]
    else:
        q = [s]

    total = 0
    for current in q:
        if "_" not in current[-2:]:
            if (int(current[-2:]) % 25 == 0):
                if "_" not in current:
                    total += 1
                else:
                    total += ((10**current.count("_")) * (10-(current[0] == "_"))) // 10
        else:
            print(current, 10**((current.count("_") - current[-2:].count("_")) - (current[0] == "_")))
            total += max((((10**(current.count("_") - current[-2:].count("_"))) * (10-(current[0] == "_"))) // 10, 1)) * lastTwo(current[-2:])

    return total


s = input()
if s[0] == "0":
    print(int(s == "0"))
elif "_" not in s and "X" not in s:
    print(int((int(s) % 25) == 0))
elif s == "X" or s == "_":
    print(1)
elif s == "0":
    print(1)
elif len(s) == 1:
    print(0)
elif s == "__" or s == "_X" or s == "X_":
    print(3)
else:
    print(sPossibleCount(s))
