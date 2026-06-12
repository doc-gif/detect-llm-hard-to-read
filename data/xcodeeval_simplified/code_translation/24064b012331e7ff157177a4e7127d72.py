nine = [0, 9, 99, 999, 9999, 99999, 999999, 9999999, 99999999, 999999999]
def get_answer(n):
    if n < 5:
        return (n * (n - 1)) // 2
    if 2 * n - 1 in nine:
        return 1
    if n in nine:
        return (n - 1) // 2
    str_n = str(n)
    len_n = len(str_n)
    len_2n = len(str(2 * n - 1))
    if len_n == len_2n:
        suf_str = "9" * (len_n - 1)
        k = int(suf_str)
        res = 0
        for c in range(10):
            prefix_num = int(str(c) + suf_str)
            if prefix_num > 2 * n - 1:
                break
            if prefix_num <= n:
                for i in range(c // 2 + 1):
                    if i == c - i:
                        res += (k - 1) // 2 if i == 0 else (k + 1) // 2
                    else:
                        res += k if i == 0 else k + 1
            else:
                first_digit = int(str_n[0])
                for i in range(c // 2 + 1):
                    if i > first_digit or c - i > first_digit:
                        continue
                    if i < first_digit and c - i < first_digit:
                        if i == c - i:
                            res += (k - 1) // 2 if i == 0 else (k + 1) // 2
                        else:
                            res += k if i == 0 else k + 1
                    else:
                        if i != c - i:
                            res += n - first_digit * (k + 1) + 1
                        else:
                            suffix_val = int(str_n[1:])
                            res += get_answer(suffix_val) + (suffix_val in nine)
        return res
    else:
        suf = int("9" * len_n)
        return n - (suf + 1) // 2 + 1
print(get_answer(int(input())))