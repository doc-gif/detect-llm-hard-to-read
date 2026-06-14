from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:
    def max_depth(group: str) -> int:
        depth = max_d = 0
        for c in group:
            depth += 1 if c == "(" else -1
            max_d = max(max_d, depth)
        return max_d

    return [max_depth(g) for g in paren_string.split() if g]
