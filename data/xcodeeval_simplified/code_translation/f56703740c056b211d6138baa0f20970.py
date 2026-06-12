n = int(input())
divisors = []
divisor = 1
while divisor**2 <= n:
    if n % divisor == 0:
        divisors.append(divisor)
        divisors.append(n // divisor)
    divisor += 1
unique_divisors = set(divisors)
special_digits = {"1", "2", "3", "5", "6", "8", "9", "0"}
count = 0
for divisor in unique_divisors:
    if special_digits == special_digits - set(str(divisor)):
        count += 1
print("YES" if count > 0 else "NO")