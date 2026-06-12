def prime_factorization(number):
    factors = []
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            factors.append(divisor)
            while number % divisor == 0:
                number //= divisor
        divisor += 1
    if number > 1:
        factors.append(number)
    return factors
def main(X, N):
    result = 1
    MOD = 10**9 + 7
    primes = prime_factorization(X)
    for prime in primes:
        power = 0
        factor = prime
        while factor <= N:
            power += N // factor
            factor *= prime
        result = (result * pow(prime, power, MOD)) % MOD
    return result
x, n = map(int, input().split())
print(main(x, n))