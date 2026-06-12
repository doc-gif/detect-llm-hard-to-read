import re
a = 8
b = 5
c = 3
positions = input()
if re.search("[b-g]", positions):
    if re.search("[2-7]", positions):
        print(a)
    elif re.search("[1]", positions) or re.search("[8]", positions):
        print(b)
if re.search("[h]", positions):
    if re.search("[2-7]", positions):
        print(b)
    elif re.search("[1]", positions) or re.search("[8]", positions):
        print(c)
if re.search("[a]", positions):
    if re.search("[2-7]", positions):
        print(b)
    elif re.search("[1]", positions) or re.search("[8]", positions):
        print(c)