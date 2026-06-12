from typing import List


def match_parens(lst: List[str]) -> str:
    def is_valid(s: str) -> bool:
        balance = 0
        for char in s:
            if char == "(":
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                return False
        return balance == 0

    s1 = lst[0] + lst[1]
    s2 = lst[1] + lst[0]
    return "Yes" if is_valid(s1) or is_valid(s2) else "No"
