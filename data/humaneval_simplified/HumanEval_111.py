from typing import Dict


def histogram(test: str) -> Dict[str, int]:
    if not test:
        return {}
    words = [w for w in test.split() if w]
    if not words:
        return {}
    max_count = max(words.count(word) for word in set(words))
    return {word: max_count for word in set(words) if words.count(word) == max_count}
