import math
n = int(input())
digit_count = 0
temp = n
while temp > 0:
    temp //= 10
    digit_count += 1
divisor = int(math.pow(10, digit_count - 1))
remainder = n % divisor
next_number = n - remainder + int(math.pow(10, digit_count - 1))
print(next_number - n)