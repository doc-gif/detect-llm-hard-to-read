from typing import List, Tuple


def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    closest_pair = None
    min_distance = None
    for i, x in enumerate(numbers):
        for j, y in enumerate(numbers):
            if i == j:
                continue
            current_distance = abs(x - y)
            if min_distance is None or current_distance < min_distance:
                min_distance = current_distance
                closest_pair = (min(x, y), max(x, y))
    return closest_pair
