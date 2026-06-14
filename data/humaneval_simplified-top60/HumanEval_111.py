from typing import Dict


def histogram(test: str) -> Dict[str, int]:
    words = [w for w in test.split() if w]
    if not words:
        return {}
    max_count = max(words.count(w) for w in set(words))
    return {w: max_count for w in set(words) if words.count(w) == max_count}
