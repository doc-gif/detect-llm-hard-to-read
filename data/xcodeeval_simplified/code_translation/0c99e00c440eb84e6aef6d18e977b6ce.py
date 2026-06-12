import math
def smallest_prime_factor(n):
    i = 2
    while i <= math.isqrt(n):
        if n % i == 0:
            return i
        if i == 2:
            i += 1
        else:
            i += 2
    return n
n = int(input())
operations = 0
while n != 0:
    factor = smallest_prime_factor(n)
    if factor == n:
        operations += 1
        break
    if n % 2 == 0:
        operations += n // 2
        break
    n -= factor
    operations += 1
print(operations)