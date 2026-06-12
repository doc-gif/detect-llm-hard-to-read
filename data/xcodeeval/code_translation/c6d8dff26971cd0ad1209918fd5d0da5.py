arrs = []
for char in input():
    if char not in arrs:
        arrs.append(char)
if len(arrs) % 2 != 0:
    print('IGNORE HIM!')
else:
    print('CHAT WITH HER!')