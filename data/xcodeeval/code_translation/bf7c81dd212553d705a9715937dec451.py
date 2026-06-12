from math import log, ceil
number = str(input())

result = ceil(len(number) / 2)

todas = True
for index, wea in enumerate(number):
    if index == 0:
        continue
    else:
        todas = todas and wea == '0'

if todas and (len(number) - 1) % 2 == 0:
    result -= 1

print(result)
