from typing import List


def skjkasdkd(lst: List[int]) -> int:
    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    max_prime = 0
    for num in lst:
        if num > max_prime and is_prime(num):
            max_prime = num
    return sum(int(digit) for digit in str(max_prime))
