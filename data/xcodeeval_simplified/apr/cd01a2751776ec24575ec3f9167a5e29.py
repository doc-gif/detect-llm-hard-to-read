from itertools import chain, combinations
from collections import defaultdict
import math


def powerset(iterable):
    items = list(iterable)
    return chain.from_iterable(combinations(items, r) for r in range(len(items) + 1))


def compute_hash(sequence):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    product = 1
    for value in sequence:
        product *= primes[value - 1]
    return product


seen_hashes = set()
total = 0
required_digits = [int(digit) for digit in "1000000000000000000"]
required_set = set(required_digits)
for subset in powerset(required_digits):
    if len(subset) == 0:
        continue
    subset_hash = compute_hash(subset)
    if subset_hash in seen_hashes:
        continue
    seen_hashes.add(subset_hash)
    frequency = defaultdict(int)
    for digit in subset:
        frequency[digit] += 1
    missing_required = any(frequency[req] == 0 for req in required_set)
    if missing_required:
        continue
    denominator = 1
    for count in frequency.values():
        denominator *= math.factorial(count)
    n = len(subset)
    total += (n - frequency[0]) * math.factorial(n - 1) / denominator
print(int(total))
