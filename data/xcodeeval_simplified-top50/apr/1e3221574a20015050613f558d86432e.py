import sys

input = sys.stdin.readline


def inp():
    return int(input())


def inlt():
    return list(map(int, input().split()))


def insr():
    s = input()
    return list(s[: len(s) - 1])


def invr():
    return map(int, input().split())


def prime_factors(n):
    factors = []
    divisor = 2
    remaining = n
    while remaining > 1:
        while remaining % divisor == 0:
            factors.append(divisor)
            remaining //= divisor
        divisor += 1
    return factors


def count_factor(factor, factors_list):
    count = 0
    for f in factors_list:
        if f == factor:
            count += 1
    return count


numbers = inlt()
a, b = numbers[0], numbers[1]
a_factors = prime_factors(a)
b_factors = prime_factors(b)
twos_a = count_factor(2, a_factors)
threes_a = count_factor(3, a_factors)
fives_a = count_factor(5, a_factors)
twos_b = count_factor(2, b_factors)
threes_b = count_factor(3, b_factors)
fives_b = count_factor(5, b_factors)
reduced_a = a // (2**twos_a * 3**threes_a * 5**fives_a)
reduced_b = b // (2**twos_b * 3**threes_b * 5**fives_b)
if reduced_a == reduced_b:
    steps = abs(fives_a - fives_b) + abs(threes_a - threes_b) + abs(twos_a - twos_b)
    print(steps)
else:
    print(-1)
