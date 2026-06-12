def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    i = 4
    while i < limit:
        is_prime[i] = False
        i += 2
    i = 3
    while i * i <= limit:
        for j in range(i * i, limit, 2 * i):
            is_prime[j] = False
        i += 2
    primes = []
    for number in range(len(is_prime)):
        if is_prime[number]:
            primes.append(number)
    return primes


prime_list = sieve_of_eratosthenes(10**8)
n = int(input())
count = 0
factor = -1
for prime in prime_list:
    if n % prime == 0:
        count += 1
        factor = prime
if count >= 2:
    print(1)
elif count == 1:
    print(factor)
else:
    print(n)
