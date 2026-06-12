import math


def lucky_gen():
    current = ['4']
    while True:
        yield int(''.join(current))
        for i in range(len(current)-1, -1, -1):
            if current[i] == '4':
                current[i] = '7'
                break
            else:
                current[i] = '4'
                if i == 0:
                    current.insert(0, '4')


def sub_str(num):
    n_str = str(num)
    for i in range(1, len(n_str)+1):
        for j in range(len(n_str) - i + 1):
            yield n_str[j:j+i]


num = int(input())
str_num = str(num)
while num % 10 == 0:
    num //= 10

result = {}

for sub in sub_str(num):
    if sub in result.keys():
        continue
    success = False
    for i in sub:
        if not i in ['4', '7']:
            success = False
            break
    else:
        success = True
    if not success:
        continue

    i = 0
    sub_str_amount = 0
    while i < len(str_num):
        try:
            i = str_num.index(sub, i) + 1
            sub_str_amount += 1
        except ValueError:
            break
    result[sub] = sub_str_amount

answer = (0, '777')
for key in result.keys():
    if answer[0] < result[key] or (answer[0] == result[key] and answer[1] > key):
            answer = (result[key], key)
if answer[0] == 0:
    print(-1)
else:
    print(answer[1])
