import re
a = int(8)
b = int(5)
c = int(3)
positions = input()

if re.search("[b-g]", positions):
    if re.search("[2-7]", positions):
        print(a)
    elif re.search("[1]", positions):
        print(b)
    elif re.search("[8]", positions):
        print(b)

if re.search("[h]", positions):
    if re.search("[2-7]", positions):
        print(b)
    elif re.search("[1]", positions):
        print(c)
    elif re.search("[8]", positions):
        print(c)

if re.search("[a]", positions):
    if re.search("[2-7]", positions):
        print(b)
    elif re.search("[1]", positions):
        print(c)
    elif re.search("[8]", positions):
        print(c)