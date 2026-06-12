'''
Author: your name
Date: 2021-12-10 14:18:39
LastEditTime: 2021-12-13 21:22:52
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /code_everyWeek/week3.py
'''

def solution_1(input_str):
    if len(input_str) >= 2 and input_str[0] == '0':
        return 0

    if 'X' not in input_str and '_' not in input_str:
        input_num = int(input_str)
        if input_num % 25 == 0:
            return 1
        else:
            return 0

    if len(input_str) == 1:
        if input_str in ['0', 'X', '_']:
            return 1
        else:
            return 0
            
    X_ = False
    last_two_num = 0

    if input_str[-1] not in ['0', '5', 'X', '_']:
        return 0

    if input_str[-1] == '5':
        if input_str[-2] in ['2', '7']:
            last_two_num = 1
        elif input_str[-2] == 'X':
            last_two_num = 2
            X_ = True # ====== 
        elif input_str[-2] == '_':
            last_two_num = 2
        else:
            return 0

    if input_str[-1] == '0':
        if input_str[-2] in ['5', '0']:
            last_two_num = 1
        elif input_str[-2] == 'X':
            if input_str[0] != 'X':
                last_two_num = 2 # 
            else:
                last_two_num = 1 # 
            X_ = True
        elif input_str[-2] == '_':
            last_two_num = 2
            if len(input_str) != 2:
                last_two_num = 2 # 
            else:
                last_two_num = 1 # 
        else:
            return 0

    if input_str[-1] == 'X':
        if input_str[-2] in ['2', '7']:
            last_two_num = 1 # 'X'=5
            X_ = True
        elif input_str[-2] in ['5', '0']:
            if input_str[0] != 'X':
                last_two_num = 2 # 'X' 0/5
                X_ = True
            else:
                return 0
        elif input_str[-2] == '_':
            if input_str[0] == 'X':
                last_two_num = 2 # 25 / 75
            elif len(input_str) == 2:
                last_two_num = 3 # 25 / 75 / 50
            else:
                last_two_num = 4 # 25 / 75/ 50 / 00
            X_ = True
        elif input_str[-2] == 'X':
            if input_str[0] == 'X':
                return 0
            else:
                last_two_num = 1 # 00
                X_ = True
        else:
            return 0

    if input_str[-1] == '_':
        if input_str[-2] in ['2', '5', '7', '0']:
            last_two_num = 1
        elif input_str[-2] == '_':
            if len(input_str) != 2:
                last_two_num = 4 # 25/75/50/00
            else:
                last_two_num = 3 # 25/75/50
        elif input_str[-2] == 'X':
            if input_str[0] == 'X':
                last_two_num = 3 # 25 / 75 / 50
            else:
                last_two_num = 4
            X_ = True
        else:
            return 0

    if len(input_str) <= 2:
        return last_two_num


    num_of_ = 0
    num_ofX = 0
    for i in range(0, len(input_str)-2):
        if input_str[i] == '_':
            num_of_ += 1
        elif input_str[i] == 'X':
            num_ofX += 1

    if input_str[0] != '_':
        res = pow(10, num_of_) * (10 if num_ofX and not X_ else 1) * last_two_num
    else:
        res = 9 * pow(10, max(num_of_-1, 0)) * (10 if num_ofX and not X_ else 1) * last_two_num

    return res


if __name__ == "__main__":
    input_str = input()
    res = solution_1(input_str)
    print(res)
