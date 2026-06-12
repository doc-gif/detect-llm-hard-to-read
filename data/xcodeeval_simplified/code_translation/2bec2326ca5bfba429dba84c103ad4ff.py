n = int(input())
i = 2
result = 1
while i * i <= n:
    if n % i == 0:
        result *= i
        while n % i == 0:
            n //= i
    i += 1
if n > 1:
    result *= n
print(result)