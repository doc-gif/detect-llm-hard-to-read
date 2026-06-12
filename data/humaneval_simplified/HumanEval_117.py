from typing import List


def select_words(s: str, n: int) -> List[str]:
    vowels = {"a", "e", "i", "o", "u"}
    result = []
    for word in s.split():
        consonant_count = sum(1 for ch in word if ch.lower() not in vowels)
        if consonant_count == n:
            result.append(word)
    return result
