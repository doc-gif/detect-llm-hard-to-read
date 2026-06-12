import math
n = int(input())
x = n
factors = [x]
for i in range(2, int(math.sqrt(n)) + 1):
    while n % i == 0:
        factors.append(n // i)
        n = n // i
if factors[-1] != 1:
    factors.append(1)
for i in range(len(factors) - 1):
    print(factors[i], end=" ")
print(factors[-1])