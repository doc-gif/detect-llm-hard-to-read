def solution_1(input_str):
    if len(input_str) >= 2 and input_str[0] == "0":
        return 0
    if "X" not in input_str and "_" not in input_str:
        return 1 if int(input_str) % 25 == 0 else 0
    if len(input_str) == 1:
        return 1 if input_str in ["0", "X", "_"] else 0
    if input_str[-1] not in ["0", "5", "X", "_"]:
        return 0
    X_ = False
    last_two_num = 0
    if input_str[-1] == "5":
        if input_str[-2] in ["2", "7"]:
            last_two_num = 1
        elif input_str[-2] == "X":
            last_two_num = 2
            X_ = True
        elif input_str[-2] == "_":
            last_two_num = 2
        else:
            return 0
    if input_str[-1] == "0":
        if input_str[-2] in ["5", "0"]:
            last_two_num = 1
        elif input_str[-2] == "X":
            last_two_num = 2 if input_str[0] != "X" else 1
            X_ = True
        elif input_str[-2] == "_":
            last_two_num = 2 if len(input_str) != 2 else 1
        else:
            return 0
    if input_str[-1] == "X":
        if input_str[-2] in ["2", "7"]:
            last_two_num = 1
            X_ = True
        elif input_str[-2] in ["5", "0"]:
            if input_str[0] != "X":
                last_two_num = 2
                X_ = True
            else:
                return 0
        elif input_str[-2] == "_":
            if input_str[0] == "X":
                last_two_num = 2
            elif len(input_str) == 2:
                last_two_num = 3
            else:
                last_two_num = 4
            X_ = True
        elif input_str[-2] == "X":
            if input_str[0] == "X":
                return 0
            else:
                last_two_num = 1
                X_ = True
        else:
            return 0
    if input_str[-1] == "_":
        if input_str[-2] in ["2", "5", "7", "0"]:
            last_two_num = 1
        elif input_str[-2] == "_":
            last_two_num = 4 if len(input_str) != 2 else 3
        elif input_str[-2] == "X":
            last_two_num = 3 if input_str[0] == "X" else 4
            X_ = True
        else:
            return 0
    if len(input_str) <= 2:
        return last_two_num
    num_of_ = 0
    num_ofX = 0
    for i in range(len(input_str) - 2):
        if input_str[i] == "_":
            num_of_ += 1
        elif input_str[i] == "X":
            num_ofX += 1
    if input_str[0] != "_":
        res = pow(10, num_of_) * (10 if num_ofX and not X_ else 1) * last_two_num
    else:
        res = (
            9
            * pow(10, max(num_of_ - 1, 0))
            * (10 if num_ofX and not X_ else 1)
            * last_two_num
        )
    return res


if __name__ == "__main__":
    input_str = input()
    res = solution_1(input_str)
    print(res)
