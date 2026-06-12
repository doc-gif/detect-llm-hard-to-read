import math

str1 = input()
str2 = input()
value = 0
value_2 = 0
unknown = 0
for char in str1:
    if char == "+":
        value += 1
    else:
        value -= 1
for char in str2:
    if char == "+":
        value_2 += 1
    elif char == "-":
        value_2 -= 1
    else:
        unknown += 1
plus_count = 0
minus_count = 0
rav = 0
x = value - value_2
if x <= unknown:
    if x >= 0:
        plus_count += x
        rav = unknown - plus_count
    else:
        minus_count += x
        rav = unknown - minus_count
    if plus_count == 0 and minus_count == 0 and rav == 0:
        print("1.000000000000")
    else:
        if rav % 2 == 0:
            rav = rav // 2
            plus_count += rav
            minus_count += rav
            k = max(plus_count, minus_count)
            C = math.factorial(unknown) / (
                math.factorial(unknown - k) * math.factorial(k)
            )
            O = 2**unknown
            res = C / O
            print(f"{res:.12f}")
        else:
            print("0.000000000000")
else:
    print("0.000000000000")
