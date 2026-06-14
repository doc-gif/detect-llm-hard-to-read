from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    result = []
    current = []
    depth = 0
    for char in paren_string:
        if char == "(":
            depth += 1
            current.append(char)
        elif char == ")":
            depth -= 1
            current.append(char)
            if depth == 0:
                result.append("".join(current))
                current.clear()
    return result
