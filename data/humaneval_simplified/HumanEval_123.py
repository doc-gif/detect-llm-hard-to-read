from typing import List


def get_odd_collatz(n: int) -> List[int]:
    odd_collatz = [] if n % 2 == 0 else [n]
    while n > 1:
        n = n // 2 if n % 2 == 0 else n * 3 + 1
        if n % 2 == 1:
            odd_collatz.append(n)
    return sorted(odd_collatz)
