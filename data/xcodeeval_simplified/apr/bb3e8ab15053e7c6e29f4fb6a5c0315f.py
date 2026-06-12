import sys

input = sys.stdin.readline


def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    primes = []
    for num in range(2, limit + 1):
        if is_prime[num]:
            primes.append(num)
            for multiple in range(num, limit + 1, num):
                is_prime[multiple] = False
    return primes


n, m = map(int, input().split())
primes = sieve_of_eratosthenes(100)
ans = 1
powers_of_two = [1]
for _ in range(20):
    powers_of_two.append(2 * powers_of_two[-1])
for i in range(2, n + 1):
    valid_primes = []
    for prime in primes:
        if pow(i, prime) > n:
            break
        valid_primes.append(prime)
    ans0 = m
    for mask in range(1, powers_of_two[len(valid_primes)]):
        product = 1
        for idx in range(len(valid_primes)):
            if mask & powers_of_two[idx]:
                product *= valid_primes[idx]
            if product > m:
                break
        sign = 2 * ((bin(mask).count("1") % 2) ^ 1) - 1
        ans0 += m // product * sign
    ans += ans0
print(ans)
