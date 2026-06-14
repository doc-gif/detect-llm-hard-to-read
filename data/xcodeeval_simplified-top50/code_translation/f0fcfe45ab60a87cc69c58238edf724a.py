a = input()
b = input()
def isSubSequence(str1, str2):
    m = len(str1)
    n = len(str2)
    j = 0
    i = 0
    while j < m and i < n:
        if str1[j] == str2[i]:
            j += 1
        i += 1
    return j == m
c = a
s = 0
for char in b:
    if char not in c:
        s = -1
        break
    else:
        idx = c.index(char)
        c = c[:idx] + c[idx + 1 :]
if s == -1:
    print("need tree")
else:
    if len(b) > len(a):
        print("need tree")
    elif len(b) == len(a):
        print("array")
    else:
        if isSubSequence(b, a):
            print("automaton")
        else:
            print("both")