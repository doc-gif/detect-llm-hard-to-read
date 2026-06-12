def ListToString(x):
    string1 = ""
    return (string1.join(x))

numindex = []   
x = input()
nums = [int(n) for n in x.split()]
letters = str(input())
letterlist = list(letters)

for i in range (0, nums[1], 1):
    for j in range (0, nums[0]-1, 1):
        if (letterlist[j] == "B" and letterlist[j + 1] == "G"):
            # temp = letterlist[j]
            # letterlist[j] = letterlist[j+1]
            # letterlist[j+1] = temp
            numtemp = j
            numindex.append(numtemp)
        else:
            continue
    for k in range (0, len(numindex), 1):
        temp = letterlist[numindex[k]]
        letterlist[numindex[k]] = letterlist[numindex[k] + 1]
        letterlist[numindex[k] + 1] = temp
    numindex.clear()

print(ListToString(letterlist))


