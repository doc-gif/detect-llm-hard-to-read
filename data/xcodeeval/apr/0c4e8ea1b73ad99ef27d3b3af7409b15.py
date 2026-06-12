l1 = input().split()
l = int(l1[0])
jump = int(l1[1])
string = input()
g = string.find("G")
t = string.find("T")

if (g != 0) and g+1<len(string):
    if jump != 1 and (string[g+1]=="T" or string[g-1]=="T"):
        print("NO")
        exit()
if g==0 and g+1<len(string):
    if jump != 1 and (string[g+1]=="T"):
        print("NO")
        exit()
if g == len(string)-1:
    if jump != 1 and (string[g-1]=="T"):
        print("NO")
        exit()



if (t > g):
    while g < len(string):
        g += jump
        if string[g] == "#":
            print("NO")
            exit()
        elif string[g] == ".":
            continue
        else:
            print("YES")
            exit()
else:
    while g > 0:
        g -= jump
        if string[g] == "#":
            print("NO")
            exit()
        elif string[g] == ".":
            continue
        else:
            print("YES")
            exit()

