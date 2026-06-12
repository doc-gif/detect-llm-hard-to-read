n = int(input())
def get_factors(x):
    factors = []
    for i in range(1, int(n**0.5) + 1):
        if x % i == 0:
            factors.append(i)
    return factors
factors = get_factors(n)
b = n // factors[-1]
a = n // b
print(a, b)