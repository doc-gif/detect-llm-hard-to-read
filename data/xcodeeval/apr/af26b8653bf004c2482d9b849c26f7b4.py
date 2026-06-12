s = input()
n = len(s)

valid10 = {"0","2","5","7"}
valid1 = {"0","5"}
if n < 2:
    if s == "0" or s == "X" or s == "_":
        print("1")
    else:
        print("0")
    exit(0)

if n == 2:
    if s == "__":
        print(3)
        exit(0)
    elif s == "_X":
        print(3)
        exit(0)

if s[0] == "0":
    print(0)
    exit(0)

if s[n-2] not in valid10 and s[n-2] not in ["X","_"]:
    print("0")
    exit(0)

if s[n-1] not in valid1 and s[n-1] not in ["X","_"]:
    print("0")
    exit(0)

x = "X" in s
zero = s[0] == "X"

validX = {"0","1","2","3","4","5","6","7","8","9"}
if zero:
    validX.remove("0")

ans = 1

for i,c in enumerate(s[:-2]):
    if c == "_":
        if i == 0:
            ans *= 9
        else:
            ans *= 10
    
if s[-2] in ["2","7"] and s[-1] == "X":
    validX = validX.intersection({5})
if s[-2] in ["0","5"] and s[-1] == "X":
    validX = validX.intersection({0})
if s[-1] == "0" and s[-2] == "X":
    validX = validX.intersection({"0","5"})
if s[-1] == "5" and s[-2] == "X":
    validX = validX.intersection({"2","7"})
if s[-2:] == "XX":
    validX = validX.intersection({"0"})
if s[-2:] == "X_":
    validX = validX.intersection(valid10)
if s[-2:] == "_X":
    validX = validX.intersection(valid1)
    ans *= 2
if s[-2:] == "__":
    ans *= 4

if x:
    ans *= len(validX)
print(ans)
