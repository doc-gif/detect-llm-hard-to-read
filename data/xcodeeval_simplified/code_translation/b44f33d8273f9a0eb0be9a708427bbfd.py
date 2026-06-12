def sum_digit(num):
    total = 0
    while num > 0:
        digit = num % 10
        total += digit
        num //= 10
    return total
input_str = input()
n = int(input_str)
str_n = str(n)
if len(str_n) > 1:
    first_digit = str(int(str_n[0]) - 1)
    if first_digit == "0":
        first_digit = ""
    n1_str = first_digit + "9" * (len(str_n) - 1)
    x = int(n1_str)
    y = n - x
    print(sum_digit(x) + sum_digit(y))
else:
    print(n)